from django.db import models

class Status(models.TextChoices):
    PUBLIC = 'public', 'Public'
    PRIVATE = 'private', 'Private'


class Song(models.Model):
    prompt = models.OneToOneField('prompt.Prompt', on_delete=models.CASCADE, related_name="song")
    library = models.ForeignKey('library.Library', on_delete=models.CASCADE, related_name="song")
    
    song_name = models.CharField(max_length=50)
    image_link = models.CharField(max_length=255, null=True, blank=True)
    song_url = models.CharField(max_length=255)
    shared_link = models.CharField(max_length=255, blank=True, null=True)

    sharing_status = models.CharField(max_length=20, choices=Status.choices, default=Status.PRIVATE)
    
    description = models.TextField(blank=True, null=True)
    lyrics = models.TextField(blank=True, null=True)
    length = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        db_table = 'song'

    def __str__(self):
        return f"{self.song_name} - {self.generation_status}"