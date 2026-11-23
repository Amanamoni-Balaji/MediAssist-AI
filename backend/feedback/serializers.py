from rest_framework import serializers
from .models import Feedback

class FeedbackSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Feedback
        fields = ['id', 'user', 'username', 'conversation', 'message', 'is_helpful', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'user', 'username', 'created_at']

    def get_username(self, obj):
        return obj.user.username if obj.user else "Anonymous"

