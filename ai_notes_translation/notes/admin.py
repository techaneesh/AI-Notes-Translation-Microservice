from django.contrib import admin
from .models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'original_language', 'translated_language', 'created_at']
    list_filter = ['original_language', 'translated_language', 'created_at']
    search_fields = ['title', 'text']
    readonly_fields = ['created_at', 'updated_at']
