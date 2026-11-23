from django.db import models
from django.contrib.auth.models import User
from conversations.models import Conversation, ChatMessage

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='feedbacks')
    conversation = models.ForeignKey(Conversation, on_delete=models.SET_NULL, null=True, blank=True, related_name='feedbacks')
    message = models.ForeignKey(ChatMessage, on_delete=models.SET_NULL, null=True, blank=True, related_name='feedbacks')
    is_helpful = models.BooleanField(default=True)
    rating = models.IntegerField(default=5, help_text="Rating from 1 (poor) to 5 (excellent)")
    comment = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        status = "Helpful" if self.is_helpful else "Not Helpful"
        return f"Feedback ({status}, {self.rating} stars) by {self.user or 'Guest'}"
