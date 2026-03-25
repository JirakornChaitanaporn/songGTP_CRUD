from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Song
from .serializers import SongSerializer, SongSerializerSave
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SongForm
from django.contrib import messages
from prompt.models import Prompt
from library.models import Library

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


def create_song_template(request):
    # check if request from submit form
    if request.method == "POST":
        form = SongForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Song created successfully")
            return redirect("create_song_template")
            
    # GET
    prompts = Prompt.objects.all()
    libraries = Library.objects.all()
    return render(request, "song/create-song.html", {"prompts": prompts, "libraries": libraries})

def search_song_template(request):
    song_name = request.GET.get("song_name")
    if song_name == None or song_name == "":
        songs = Song.objects.all()
    else:
        songs = Song.objects.filter(song_name__contains=song_name)
        
    return render(request, "song/search-song.html", {"songs": songs} )

def delete_song_template(request):
    pk = request.GET.get("id")
    try:
        song = Song.objects.get(pk=pk)
        song.delete()
        messages.success(request, "Song deleted successfully")
        
    except Song.DoesNotExist:
        print(f"Song id:{pk} does not exist")
        messages.error(request, "Song cannot be deleted because this song does not exist")
        
    return redirect("search_song")

def update_song_template(request):
    pk = request.GET.get("id")
    old_song = get_object_or_404(Song, id=pk)
    if request.method == "POST":
        form = SongForm(request.POST, instance=old_song)
        if form.is_valid():
            form.save()
            messages.success(request, "Song updated successfully")
            return redirect("search_song")
        else:
            messages.error(request, "Song the input information was not complete")
            return redirect("search_song")
        
    #GET
    prompts = Prompt.objects.all()
    libraries = Library.objects.all()
    return render(request, "song/update-song.html", {"song": old_song, "prompts": prompts, "libraries": libraries})