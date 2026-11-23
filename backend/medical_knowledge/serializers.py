from rest_framework import serializers
from .models import MedicalKnowledge

class MedicalKnowledgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalKnowledge
        fields = [
            'id', 'topic', 'slug', 'category', 'description',
            'symptoms', 'causes', 'prevention', 'when_to_seek_care',
            'references', 'keywords', 'created_at', 'updated_at'
        ]

class MedicalKnowledgeSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalKnowledge
        fields = ['id', 'topic', 'slug', 'category', 'symptoms']

