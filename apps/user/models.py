from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    # def create_user(self, email, password=None, **extra_fields):
    #     if not email:
    #         raise ValueError("The Email field must be set")
    #     email = self.normalize_email(email)
    #     user = self.model(email=email, **extra_fields)
    #     user.set_password(password)  # Ensures the password is hashed
    #     user.save(using=self._db)
    #     return user
    
    class Meta:
        ordering = ['created_at']
        db_table = 'user'
        
    def __str__(self):
        return f"Username: {self.username} | Email: {self.email}"