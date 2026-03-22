from django.contrib import admin
from .models import User

admin.site.register(User)
# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ['id', 'username', 'email', 'created_at']
#     list_filter = ['created_at']
#     search_fields = ['username', 'email']
#     readonly_fields = ['created_at']
#     ordering = ['-created_at']
    
#     fieldsets = (
#         ('User Information', {
#             'fields': ('username', 'email')
#         }),
#         ('Timestamps', {
#             'fields': ('created_at',),
#             'classes': ('collapse',)
#         }),
#     )
