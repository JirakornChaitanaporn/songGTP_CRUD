from rest_framework import serializers
from .models import Library
from user.serializers import UserSerializer

class LibrarySerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Library
        fields = ['id', 'user', 'created_at']
        read_only_fields = ['created_at']

class LibrarySerializerSave(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = ['id', 'user', 'created_at']
        read_only_fields = ['created_at']