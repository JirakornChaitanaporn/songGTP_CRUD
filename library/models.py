from django.db import models
from user.models import User

# Create your models here.
class Library(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name="library")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
        db_table = 'library'
        
    def __str__(self):
        return f"This library belongs to: {self.user.username}"