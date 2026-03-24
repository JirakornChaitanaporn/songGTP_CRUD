from django.forms import ModelForm
from .models import Song

class SongForm(ModelForm):
    class Meta:
        model = Song
        fields = ["prompt", "library", "song_name", "shared_link", "sharing_status", "generation_status","song_url","description","lyrics"]