from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Song
from .serializers import SongSerializer, SongSerializerSave

# Create your views here.
@api_view(["GET"])
def get_song(request):
    songs = Song.objects.all()
    serializer = SongSerializer(songs, many = True)
    return Response(serializer.data)

@api_view(["POST"])
def create_song(request):
    body = request.data
    serializer = SongSerializerSave(data=body)
    if serializer.is_valid():
        serializer.save() # INSERT 
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["PUT"])
def update_song(request, pk) :
    body = request.data
    try:
        song = Song.objects.get(pk=pk)
    except Song.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = SongSerializerSave(song, data=body)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def delete_song(request, pk):
    try:
        song = Song.objects.get(pk=pk)
    except Song.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    song.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
