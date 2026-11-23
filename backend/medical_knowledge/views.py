from rest_framework import views, status, permissions
from rest_framework.response import Response
from django.db.models import Q
from .models import MedicalKnowledge
from .serializers import MedicalKnowledgeSerializer

class MedicalKnowledgeListView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        query = request.query_params.get('search', '').strip()
        category = request.query_params.get('category', '').strip()
        
        queryset = MedicalKnowledge.objects.all()
        if category:
            queryset = queryset.filter(category__iexact=category)
        if query:
            queryset = queryset.filter(
                Q(topic__icontains=query) |
                Q(description__icontains=query) |
                Q(keywords__icontains=query)
            )
        
        serializer = MedicalKnowledgeSerializer(queryset, many=True)
        return Response(serializer.data)

class MedicalKnowledgeDetailView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, slug):
        try:
            item = MedicalKnowledge.objects.get(slug=slug)
            return Response(MedicalKnowledgeSerializer(item).data)
        except MedicalKnowledge.DoesNotExist:
            return Response({'error': 'Medical topic not found.'}, status=status.HTTP_404_NOT_FOUND)

class SymptomDictionaryView(views.APIView):
    """Returns a deduplicated, sorted list of recognized symptoms and common categories."""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        records = MedicalKnowledge.objects.all()
        symptom_set = set()
        categories = set()
        for rec in records:
            categories.add(rec.category)
            if isinstance(rec.symptoms, list):
                for s in rec.symptoms:
                    symptom_set.add(s.strip().lower())
        
        return Response({
            'symptoms': sorted(list(symptom_set)),
            'categories': sorted(list(categories))
        })

class SymptomAnalyzerView(views.APIView):
    """
    Symptom educational assessment.
    Takes user input symptoms, identifies related educational topics,
    highlights warning signs, and clearly states it is an educational tool,
    never a diagnosis.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        user_symptoms = request.data.get('symptoms', [])
        free_text = request.data.get('free_text', '').strip()

        if isinstance(user_symptoms, str):
            user_symptoms = [s.strip().lower() for s in user_symptoms.split(',') if s.strip()]
        else:
            user_symptoms = [s.strip().lower() for s in user_symptoms if isinstance(s, str) and s.strip()]

        if not user_symptoms and not free_text:
            return Response({'error': 'Please provide at least one symptom or describe how you feel.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check for emergency signs
        emergency_triggers = [
            'crushing chest pain', 'chest pressure', 'radiating pain to arm', 'difficulty breathing',
            'can\'t breathe', 'stroke', 'face drooping', 'slurred speech', 'arm weakness',
            'coughing up blood', 'suicidal', 'severe allergic reaction', 'anaphylaxis',
            'unconscious', 'seizure', 'stiff neck with high fever'
        ]
        
        combined_text = " ".join(user_symptoms) + " " + free_text.lower()
        is_emergency = any(trigger in combined_text for trigger in emergency_triggers)

        records = MedicalKnowledge.objects.all()
        matched_conditions = []

        for rec in records:
            rec_symptoms = [s.lower() for s in rec.symptoms if isinstance(s, str)]
            # Count overlap
            overlap = []
            for s in user_symptoms:
                if any(s in rs or rs in s for rs in rec_symptoms):
                    overlap.append(s)

            # Also check if topic/keywords mentioned in free_text
            topic_mentioned = rec.topic.lower() in free_text.lower() or rec.slug in free_text.lower()

            if overlap or topic_mentioned:
                matched_conditions.append({
                    'topic': rec.topic,
                    'slug': rec.slug,
                    'category': rec.category,
                    'description': rec.description,
                    'matching_symptoms': overlap,
                    'all_associated_symptoms': rec.symptoms,
                    'when_to_seek_care': rec.when_to_seek_care,
                    'overlap_score': len(overlap) + (2 if topic_mentioned else 0)
                })

        # Sort by overlap score descending
        matched_conditions.sort(key=lambda x: x['overlap_score'], reverse=True)

        return Response({
            'is_emergency': is_emergency,
            'emergency_message': (
                "EMERGENCY ADVISORY: Your query may contain signs of a medical emergency (such as severe chest pain, breathing difficulty, or neurological signs). "
                "Please call emergency services (e.g. 911, 999, 112) or go to the nearest emergency department immediately."
            ) if is_emergency else None,
            'input_symptoms': user_symptoms,
            'identified_conditions': matched_conditions[:6],
            'general_guidance': (
                "These health topics share one or more symptoms you provided. "
                "Multiple distinct health conditions can cause similar symptoms. "
                "This assessment is strictly educational and is not a medical diagnosis."
            ),
            'recommended_actions': [
                "Track the duration, severity, and any triggers for your symptoms.",
                "Consult a licensed healthcare provider for physical examination and accurate clinical diagnosis.",
                "Seek urgent medical evaluation if you experience high fever, severe unremitting pain, shortness of breath, or sudden weakness."
            ],
            'disclaimer': "This tool does not provide medical diagnoses, treatment plans, or prescriptions. Always seek the advice of a qualified healthcare professional with any questions regarding medical conditions."
        })
