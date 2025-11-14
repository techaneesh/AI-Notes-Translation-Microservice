from rest_framework import serializers
from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    """Serializer for Note model"""
    
    class Meta:
        model = Note
        fields = ['id', 'title', 'text', 'original_language', 
                  'translated_text', 'translated_language', 
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class NoteCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating notes"""
    
    class Meta:
        model = Note
        fields = ['title', 'text', 'original_language']
    
    def validate_original_language(self, value):
        """Validate language code"""
        if not value or len(value) != 2:
            raise serializers.ValidationError("Language code must be 2 characters (e.g., 'en', 'hi')")
        return value.lower()


class TranslationSerializer(serializers.Serializer):
    """Serializer for translation request"""
    target_language = serializers.CharField(max_length=10, required=True)
    
    def validate_target_language(self, value):
        """Validate target language code"""
        if not value or len(value) != 2:
            raise serializers.ValidationError("Target language code must be 2 characters (e.g., 'en', 'hi')")
        return value.lower()


class FileUploadSerializer(serializers.Serializer):
    """Serializer for file upload"""
    file = serializers.FileField(required=True)
    title = serializers.CharField(max_length=200, required=False, allow_blank=True)
    original_language = serializers.CharField(max_length=10, default='en', required=False)
    
    def validate_file(self, value):
        """Validate uploaded file"""
        # Check file size (max 5MB)
        max_size = 5 * 1024 * 1024  # 5MB
        if value.size > max_size:
            raise serializers.ValidationError("File size cannot exceed 5MB")
        
        # Check file extension
        if not value.name.lower().endswith('.txt'):
            raise serializers.ValidationError("Only .txt files are allowed")
        
        return value
    
    def validate_original_language(self, value):
        """Validate language code"""
        if value and len(value) != 2:
            raise serializers.ValidationError("Language code must be 2 characters (e.g., 'en', 'hi')")
        return value.lower() if value else 'en'

