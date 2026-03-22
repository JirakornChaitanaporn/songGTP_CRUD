from rest_framework import serializers
from .models import User, Prompt, Library, Song, Folder


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'created_at']
        read_only_fields = ['created_at']


class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = ['id', 'user', 'created_at']
        read_only_fields = ['created_at']


class PromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prompt
        fields = ['id', 'song_name', 'song_genre', 'song_mood', 'song_base_singer', 
                  'description', 'lyrics', 'keywords', 'created_at']
        read_only_fields = ['created_at']


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['id', 'prompt', 'library', 'song_name', 'shared_link', 
                  'sharing_status', 'generation_status', 'song_url', 'created_at']
        read_only_fields = ['created_at']


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ['id']
