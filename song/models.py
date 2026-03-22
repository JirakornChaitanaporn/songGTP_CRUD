from django.db import models
from library.models import Library
from prompt.models import Prompt

# Create your models here.
class Status(models.TextChoices):
    PUBLIC = 'public', 'Public'
    PRIVATE = 'private', 'Private'

class Generation(models.TextChoices):
    GENERATING = 'generating', 'Generating'
    GENERATED = 'generated', 'Generated'
    ERROR = 'error', 'Error'

class Song(models.Model):
    prompt = models.OneToOneField(Prompt,on_delete=models.CASCADE, related_name="song")
    library = models.ForeignKey(Library,on_delete=models.CASCADE, related_name="song")
    song_name = models.CharField(max_length=50)
    shared_link = models.CharField(max_length=255, blank=True, null=True)
    sharing_status = models.CharField(max_length=20, choices=Status.choices, default=Status.PRIVATE)
    generation_status = models.CharField(max_length=20, choices=Generation.choices, default=Generation.GENERATING)
    song_url = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    lyrics = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
        db_table = 'song'
        
    def __str__(self):
        return f"Song name: {self.song_name}"