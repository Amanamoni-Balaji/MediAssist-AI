from django.db import models

class MedicalKnowledge(models.Model):
    topic = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.CharField(max_length=100)
    description = models.TextField()
    symptoms = models.JSONField(default=list, help_text="List of associated symptoms")
    causes = models.TextField()
    prevention = models.TextField()
    when_to_seek_care = models.TextField(help_text="Warning signs and emergency criteria")
    references = models.JSONField(default=list, help_text="List of citations from WHO, MedlinePlus, NHS")
    keywords = models.TextField(help_text="Comma-separated synonyms and keywords for search and NLP matching")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['topic']
        verbose_name_plural = 'Medical Knowledge Records'

    def __str__(self):
        return f"{self.topic} ({self.category})"
