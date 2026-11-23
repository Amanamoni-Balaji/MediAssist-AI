import json
from django.db import models
from django.utils import timezone

class ChatbotAnalytics(models.Model):
    date = models.DateField(default=timezone.now, unique=True)
    total_queries = models.IntegerField(default=0)
    emergency_queries = models.IntegerField(default=0)
    positive_feedback = models.IntegerField(default=0)
    negative_feedback = models.IntegerField(default=0)
    total_ratings_sum = models.IntegerField(default=0)
    total_ratings_count = models.IntegerField(default=0)
    intent_distribution = models.JSONField(default=dict)
    topic_distribution = models.JSONField(default=dict)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Analytics {self.date}: {self.total_queries} queries"

    @classmethod
    def get_today_record(cls):
        today = timezone.now().date()
        record, _ = cls.objects.get_or_create(date=today)
        return record

    @classmethod
    def record_query(cls, is_emergency: bool = False, intent: str = "unknown", topic: str = None):
        record = cls.get_today_record()
        record.total_queries += 1
        if is_emergency:
            record.emergency_queries += 1

        # Update intent count
        intents = record.intent_distribution or {}
        intents[intent] = intents.get(intent, 0) + 1
        record.intent_distribution = intents

        # Update topic count
        if topic:
            topics = record.topic_distribution or {}
            topics[topic] = topics.get(topic, 0) + 1
            record.topic_distribution = topics

        record.save()

    @classmethod
    def record_feedback(cls, is_helpful: bool, rating: int):
        record = cls.get_today_record()
        if is_helpful:
            record.positive_feedback += 1
        else:
            record.negative_feedback += 1
        record.total_ratings_sum += rating
        record.total_ratings_count += 1
        record.save()
