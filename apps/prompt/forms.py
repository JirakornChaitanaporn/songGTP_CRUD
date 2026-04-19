from django.forms import ModelForm
from .models import Prompt

class PromptForm(ModelForm):
    class Meta:
        model = Prompt
        fields = ["song_name", "song_genre", "song_mood", "description", "lyrics","keywords"]