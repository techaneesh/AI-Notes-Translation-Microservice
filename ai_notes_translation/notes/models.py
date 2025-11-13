from django.db import models
from django.utils import timezone


class Note(models.Model):
    """Model to store notes with original and translated text"""
    
    title = models.CharField(max_length=200)
    text = models.TextField()
    original_language = models.CharField(max_length=10, default='en')  # Language code (en, hi, etc.)
    translated_text = models.TextField(blank=True, null=True)
    translated_language = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['original_language']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.original_language})"
