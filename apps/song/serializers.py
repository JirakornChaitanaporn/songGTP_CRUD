from rest_framework import serializers
from .models import Song
from apps.prompt.serializers import PromptSerializer
from apps.library.serializers import LibrarySerializer


class SongSerializerSave(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['id', 'prompt', 'library', 'song_name', 'image_link', 'shared_code', 
                  'sharing_status', 'song_url', 'description', 'lyrics', 'length', 'created_at']
        read_only_fields = ['created_at']

class SongSerializer(serializers.ModelSerializer):
    prompt = PromptSerializer()
    library = LibrarySerializer()
    class Meta:
        model = Song
        fields = ['id', 'prompt', 'library', 'song_name', 'image_link', 'shared_code', 
                  'sharing_status', 'song_url', 'description', 'lyrics', 'length', 'created_at']
        read_only_fields = ['created_at']
