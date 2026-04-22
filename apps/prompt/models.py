from django.db import models

# Create your models here.
class Mood(models.TextChoices):
    HAPPY = 'happy', 'Happy'
    SAD = 'sad', 'Sad'
    ROMANTIC = 'romantic', 'Romantic'
    ANGRY = 'angry', 'Angry'
    ENERGETIC = 'energetic', 'ENERGETIC'
    CALM = 'calm', 'Calm'
    
class Genre(models.TextChoices):
    POP = 'pop', 'Pop'
    ROCK = 'rock', 'Rock'
    HEAVY_METAL = 'heavy_metal', 'Heavy_metal'
    SOFT_ROCK = 'soft_rock', 'Soft_rock'
    POP_ROCK = 'pop_rock', 'Pop_rock'
    COUNTRY = 'country', 'Country'
    
class Generation(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    TEXT_SUCCESS = 'TEXT_SUCCESS', 'Text Success'   # Lyrics/Metadata generated
    FIRST_SUCCESS = 'FIRST_SUCCESS', 'First Success' # First clip of the pair ready
    SUCCESS = 'SUCCESS', 'Success'                   # Everything finished
    ERROR = 'ERROR', 'Error'
    

class Prompt(models.Model):
    task_id = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey('user.User',on_delete=models.CASCADE, related_name="prompt", blank=True, null=True)
    song_name = models.CharField(max_length=50)
    song_genre = models.CharField(max_length=20, choices=Genre.choices, default=Genre.POP)
    song_mood = models.CharField(max_length=20, choices=Mood.choices, default=Mood.HAPPY)
    generation_status = models.CharField(max_length=20, choices=Generation.choices, default=Generation.PENDING)
    description = models.CharField(max_length=255)
    lyrics = models.TextField(blank= True, null=True)
    keywords = models.TextField(blank= True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
        db_table = 'prompt'
        
    def __str__(self):
        return f"Song name: {self.song_name}| Genre: {self.song_genre}| Mood: {self.song_mood}\n \
        Description: {self.description}| Lyrics: {self.lyrics}\n \
        Keywords: {self.keywords}"
