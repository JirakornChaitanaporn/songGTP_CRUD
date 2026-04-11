from django.contrib import admin
from .models import Prompt, Genre, Mood

admin.site.register(Prompt)
# @admin.register(Prompt)
# class PromptAdmin(admin.ModelAdmin):
#     list_display = ['id', 'song_name', 'song_genre', 'song_mood', 'song_base_singer', 'created_at']
#     list_filter = ['song_genre', 'song_mood', 'created_at']
#     search_fields = ['song_name', 'song_base_singer', 'keywords']
#     readonly_fields = ['created_at']
#     ordering = ['-created_at']
    
#     fieldsets = (
#         ('Song Details', {
#             'fields': ('song_name', 'song_genre', 'song_mood', 'song_base_singer')
#         }),
#         ('Content', {
#             'fields': ('description', 'lyrics', 'keywords')
#         }),
#         ('Timestamps', {
#             'fields': ('created_at',),
#             'classes': ('collapse',)
#         }),
#     )
