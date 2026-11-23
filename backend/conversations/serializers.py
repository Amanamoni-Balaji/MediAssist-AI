from rest_framework import serializers
from .models import Conversation, ChatMessage

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = [
            'id', 'conversation', 'sender', 'text', 'intent',
            'confidence', 'entities', 'is_emergency', 'matched_topic',
            'suggested_questions', 'created_at'
        ]

class ConversationSerializer(serializers.ModelSerializer):
    message_count = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'user', 'title', 'is_active', 'message_count', 'last_message', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def get_message_count(self, obj):
        return obj.messages.count()

    def get_last_message(self, obj):
        last = obj.messages.last()
        if last:
            return {
                'text': last.text[:80],
                'sender': last.sender,
                'created_at': last.created_at
            }
        return None

class ConversationDetailSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'user', 'title', 'is_active', 'messages', 'created_at', 'updated_at']

