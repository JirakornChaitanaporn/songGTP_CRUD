from django.contrib import admin
from .models import Library

admin.site.register(Library)
# @admin.register(Library)
# class LibraryAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user', 'created_at']
#     list_filter = ['created_at']
#     search_fields = ['user__username', 'user__email']
#     readonly_fields = ['created_at']
#     ordering = ['-created_at']
    
#     fieldsets = (
#         ('Library Information', {
#             'fields': ('user',)
#         }),
#         ('Timestamps', {
#             'fields': ('created_at',),
#             'classes': ('collapse',)
#         }),
#     )
