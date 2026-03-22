from rest_framework import serializers
from .models import Song
from prompt.serializers import PromptSerializer
from library.serializers import LibrarySerializer


class SongSerializerSave(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['id', 'prompt', 'library', 'song_name', 'shared_link', 
                  'sharing_status', 'generation_status', 'song_url', 'created_at']
        read_only_fields = ['created_at']

class SongSerializer(serializers.ModelSerializer):
    prompt = PromptSerializer()
    library = LibrarySerializer()
    class Meta:
        model = Song
        fields = ['id', 'prompt', 'library', 'song_name', 'shared_link', 
                  'sharing_status', 'generation_status', 'song_url', 'created_at']
        read_only_fields = ['created_at']
