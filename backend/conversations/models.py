import uuid
from django.db import models
from django.contrib.auth.models import User

class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations', null=True, blank=True)
    title = models.CharField(max_length=255, default="New Conversation")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        username = self.user.username if self.user else "Anonymous"
        return f"{self.title} ({username}) [{self.id}]"


class ChatMessage(models.Model):
    SENDER_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)
    text = models.TextField()
    intent = models.CharField(max_length=100, blank=True, default='')
    confidence = models.FloatField(default=0.0)
    entities = models.JSONField(default=dict, blank=True)
    is_emergency = models.BooleanField(default=False)
    matched_topic = models.CharField(max_length=200, blank=True, null=True)
    suggested_questions = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"[{self.sender}] {self.text[:40]}..."
