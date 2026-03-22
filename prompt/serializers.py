from rest_framework import serializers
from .models import Prompt


class PromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prompt
        fields = ['id', 'song_name', 'song_genre', 'song_mood', 'song_base_singer', 
                  'description', 'lyrics', 'keywords', 'created_at']
        read_only_fields = ['created_at']
