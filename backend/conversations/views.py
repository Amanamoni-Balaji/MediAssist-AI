import uuid
from rest_framework import views, status, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Conversation, ChatMessage
from .serializers import ConversationSerializer, ConversationDetailSerializer, ChatMessageSerializer
from nlp_engine.service import NLPService
from analytics.models import ChatbotAnalytics

class ConversationListView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        if request.user.is_authenticated:
            conversations = Conversation.objects.filter(user=request.user)
        else:
            # For guest sessions, allow passing session ids or return empty
            session_ids = request.query_params.getlist('ids')
            if session_ids:
                conversations = Conversation.objects.filter(id__in=session_ids, user__isnull=True)
            else:
                conversations = Conversation.objects.none()

        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data)

    def post(self, request):
        title = request.data.get('title', 'New Health Consultation')
        user = request.user if request.user.is_authenticated else None
        conversation = Conversation.objects.create(user=user, title=title)
        return Response(ConversationSerializer(conversation).data, status=status.HTTP_201_CREATED)


class ConversationDetailView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        conversation = get_object_or_404(Conversation, pk=pk)
        if conversation.user and request.user != conversation.user and not request.user.is_staff:
            return Response({'error': 'Unauthorized access to conversation.'}, status=status.HTTP_403_FORBIDDEN)
        return Response(ConversationDetailSerializer(conversation).data)

    def delete(self, request, pk):
        conversation = get_object_or_404(Conversation, pk=pk)
        if conversation.user and request.user != conversation.user and not request.user.is_staff:
            return Response({'error': 'Unauthorized to delete this conversation.'}, status=status.HTTP_403_FORBIDDEN)
        conversation.delete()
        return Response({'message': 'Conversation deleted successfully.'}, status=status.HTTP_200_OK)


class ClearConversationView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, pk):
        conversation = get_object_or_404(Conversation, pk=pk)
        if conversation.user and request.user != conversation.user and not request.user.is_staff:
            return Response({'error': 'Unauthorized.'}, status=status.HTTP_403_FORBIDDEN)
        conversation.messages.all().delete()
        return Response({'message': 'Conversation messages cleared.'}, status=status.HTTP_200_OK)


class SendMessageView(views.APIView):
    """
    Receives user natural language message, executes complete NLP pipeline,
    records conversation history, updates analytics, and returns assistant response.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        user_text = request.data.get('message', '').strip()
        conv_id = request.data.get('conversation_id')

        if not user_text:
            return Response({'error': 'Message content cannot be empty.'}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve or create conversation
        conversation = None
        if conv_id:
            try:
                conversation = Conversation.objects.get(pk=conv_id)
            except Conversation.DoesNotExist:
                conversation = None

        if not conversation:
            user = request.user if request.user.is_authenticated else None
            initial_title = user_text[:40] + ("..." if len(user_text) > 40 else "")
            conversation = Conversation.objects.create(user=user, title=initial_title)

        # Retrieve and synchronize session context
        from conversation_context.context_manager import ContextManager
        context = ContextManager.get_or_create(str(conversation.id))
        last_bot_msg = conversation.messages.filter(sender='assistant').order_by('-created_at').first()
        if last_bot_msg and last_bot_msg.matched_topic and not context.active_topic:
            context.active_topic = last_bot_msg.matched_topic

        # Save user message
        user_msg = ChatMessage.objects.create(
            conversation=conversation,
            sender='user',
            text=user_text
        )

        # Process through NLP Service with conversation context
        nlp_service = NLPService.get_instance()
        nlp_result = nlp_service.process_message(user_text, conversation_id=str(conversation.id))

        # Save assistant message
        bot_msg = ChatMessage.objects.create(
            conversation=conversation,
            sender='assistant',
            text=nlp_result['response'],
            intent=nlp_result.get('intent', ''),
            confidence=nlp_result.get('confidence', 0.0),
            entities=nlp_result.get('entities', {}),
            is_emergency=nlp_result.get('is_emergency', False),
            matched_topic=nlp_result.get('matched_topic'),
            suggested_questions=nlp_result.get('suggested_questions', [])
        )

        # Update conversation title if default
        if conversation.title in ["New Conversation", "New Health Consultation"] or len(conversation.title) < 5:
            if nlp_result.get('matched_topic'):
                conversation.title = f"Inquiry: {nlp_result['matched_topic']}"
            else:
                words = user_text.split()[:5]
                conversation.title = " ".join(words)
            conversation.save()

        # Update analytics record
        ChatbotAnalytics.record_query(
            is_emergency=nlp_result.get('is_emergency', False),
            intent=nlp_result.get('intent', 'unknown'),
            topic=nlp_result.get('matched_topic')
        )

        return Response({
            'conversation_id': str(conversation.id),
            'conversation_title': conversation.title,
            'user_message': ChatMessageSerializer(user_msg).data,
            'assistant_message': ChatMessageSerializer(bot_msg).data,
            'nlp_metadata': {
                'intent': nlp_result.get('intent'),
                'confidence': nlp_result.get('confidence'),
                'entities': nlp_result.get('entities'),
                'is_emergency': nlp_result.get('is_emergency'),
                'matched_topic': nlp_result.get('matched_topic'),
                'suggested_questions': nlp_result.get('suggested_questions', []),
                'similarity_score': nlp_result.get('similarity_score', 0.0)
            }
        }, status=status.HTTP_200_OK)


class ChatbotInfoView(SendMessageView):
    """
    Endpoint for /api/chatbot/
    Provides information regarding chatbot capabilities and also accepts message POSTs.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({
            "service": "MediNLP AI Medical Healthcare Chatbot",
            "status": "Ready",
            "model": "Calibrated LinearSVC + TF-IDF Vectorizer",
            "usage": {
                "method": "POST",
                "endpoints": [
                    "/api/chatbot/",
                    "/api/chatbot/send/",
                    "/api/chat/chat/send/"
                ],
                "payload": {
                    "message": "Your health question (required)",
                    "conversation_id": "UUID of ongoing consultation (optional)"
                }
            },
            "sample_inquiries": [
                "What is diabetes?",
                "What are the common symptoms of fever?",
                "What is hypertension?",
                "How can I maintain a healthy lifestyle?",
                "What causes headaches?",
                "What are the symptoms of dehydration?"
            ],
            "disclaimer": "Educational healthcare information assistant. Not a medical diagnosis system or doctor."
        })

