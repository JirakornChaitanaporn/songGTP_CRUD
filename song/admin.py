from django.contrib import admin
from .models import Song, Status, Generation


admin.site.register(Song)
"""@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ['id', 'song_name', 'prompt', 'library', 'sharing_status', 'generation_status', 'created_at']
    list_filter = ['sharing_status', 'generation_status', 'created_at']
    search_fields = ['song_name', 'prompt__song_name']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Song Information', {
            'fields': ('song_name', 'prompt', 'library')
        }),
        ('Status & Sharing', {
            'fields': ('sharing_status', 'generation_status')
        }),
        ('Links', {
            'fields': ('shared_link', 'song_url')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )"""
