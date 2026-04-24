from django.forms import ModelForm
from .models import Song

class SongForm(ModelForm):
    class Meta:
        model = Song
        fields = ["prompt", "library", "song_name", "image_link", "shared_code", "sharing_status", "song_url","description","lyrics", "length"]