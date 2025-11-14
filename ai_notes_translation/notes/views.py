from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from .models import Note
from .serializers import NoteSerializer, NoteCreateSerializer, TranslationSerializer, FileUploadSerializer

# Try to import Translator, handle gracefully if not available
try:
    from googletrans import Translator
    TRANSLATOR_AVAILABLE = True
except ImportError:
    TRANSLATOR_AVAILABLE = False
    Translator = None


class NoteViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Note CRUD operations
    """
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    
    def get_serializer_class(self):
        """Use different serializer for create action"""
        if self.action == 'create':
            return NoteCreateSerializer
        return NoteSerializer
    
    def get_serializer_context(self):
        """Add request to serializer context for file URLs"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def get_queryset(self):
        """Get all notes, ordered by creation date"""
        return Note.objects.all().order_by('-created_at')
    
    def list(self, request, *args, **kwargs):
        """List all notes with caching"""
        cache_key = 'notes_list'
        cached_data = cache.get(cache_key)
        
        if cached_data is None:
            response = super().list(request, *args, **kwargs)
            # Cache for 5 minutes
            cache.set(cache_key, response.data, 300)
            return response
        return Response(cached_data)
    
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a single note with caching"""
        note_id = kwargs.get('pk')
        cache_key = f'note_{note_id}'
        cached_data = cache.get(cache_key)
        
        if cached_data is None:
            response = super().retrieve(request, *args, **kwargs)
            # Cache for 5 minutes
            cache.set(cache_key, response.data, 300)
            return response
        return Response(cached_data)
    
    def create(self, request, *args, **kwargs):
        """Create a new note"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Invalidate list cache
        cache.delete('notes_list')
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, *args, **kwargs):
        """Update a note"""
        response = super().update(request, *args, **kwargs)
        
        # Invalidate caches
        note_id = kwargs.get('pk')
        cache.delete(f'note_{note_id}')
        cache.delete('notes_list')
        
        return response
    
    def destroy(self, request, *args, **kwargs):
        """Delete a note"""
        note_id = kwargs.get('pk')
        response = super().destroy(request, *args, **kwargs)
        
        # Invalidate caches
        cache.delete(f'note_{note_id}')
        cache.delete('notes_list')
        
        return response
    
    @action(detail=True, methods=['post'], url_path='translate')
    def translate(self, request, pk=None):
        """
        Translate a note to target language
        POST /api/notes/{id}/translate/
        Body: {"target_language": "hi"}
        """
        note = get_object_or_404(Note, pk=pk)
        
        # Validate request data
        serializer = TranslationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        target_language = serializer.validated_data['target_language']
        
        # Check if same language
        if note.original_language.lower() == target_language.lower():
            return Response(
                {'error': 'Target language cannot be the same as original language'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check cache first
        cache_key = f'translation_{note.id}_{target_language}'
        cached_translation = cache.get(cache_key)
        
        if cached_translation:
            # Update note with cached translation
            note.translated_text = cached_translation['translated_text']
            note.translated_language = target_language
            note.save(update_fields=['translated_text', 'translated_language', 'updated_at'])
            
            return Response({
                'id': note.id,
                'title': note.title,
                'original_text': note.text,
                'original_language': note.original_language,
                'translated_text': note.translated_text,
                'translated_language': note.translated_language,
                'cached': True
            })
        
        # Perform translation using googletrans
        if not TRANSLATOR_AVAILABLE:
            return Response(
                {'error': 'Translation service is not available. Please install googletrans.'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        try:
            translator = Translator()
            translated = translator.translate(
                note.text,
                src=note.original_language,
                dest=target_language
            )
            
            # Save translation to database
            note.translated_text = translated.text
            note.translated_language = target_language
            note.save(update_fields=['translated_text', 'translated_language', 'updated_at'])
            
            # Cache the translation
            translation_data = {
                'translated_text': translated.text,
                'translated_language': target_language
            }
            cache.set(cache_key, translation_data, 3600)  # Cache for 1 hour
            
            # Invalidate note cache
            cache.delete(f'note_{note.id}')
            
            return Response({
                'id': note.id,
                'title': note.title,
                'original_text': note.text,
                'original_language': note.original_language,
                'translated_text': note.translated_text,
                'translated_language': note.translated_language,
                'cached': False
            })
            
        except Exception as e:
            return Response(
                {'error': f'Translation failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'], url_path='upload')
    def upload_file(self, request):
        """
        Upload a .txt file and create a note from its content
        POST /api/notes/upload/
        Body: multipart/form-data with 'file' field
        Optional: 'title', 'original_language'
        """
        serializer = FileUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        uploaded_file = serializer.validated_data['file']
        title = serializer.validated_data.get('title', '')
        original_language = serializer.validated_data.get('original_language', 'en')
        
        try:
            # Read file content
            # Handle both text and binary mode
            try:
                # Try to decode as UTF-8
                file_content = uploaded_file.read().decode('utf-8')
            except UnicodeDecodeError:
                # If UTF-8 fails, try with error handling
                uploaded_file.seek(0)  # Reset file pointer
                file_content = uploaded_file.read().decode('utf-8', errors='ignore')
            
            # Use filename as title if title not provided
            if not title:
                title = uploaded_file.name.replace('.txt', '').replace('_', ' ').title()
            
            # Create note from file content
            note = Note.objects.create(
                title=title,
                text=file_content.strip(),
                original_language=original_language
            )
            
            # Invalidate list cache
            cache.delete('notes_list')
            
            # Return created note
            response_serializer = NoteSerializer(note)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': f'Failed to process file: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
