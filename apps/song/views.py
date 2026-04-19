from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Song, Status
from .serializers import SongSerializer, SongSerializerSave
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SongForm
from django.contrib import messages
from apps.prompt.models import Prompt, Generation
from apps.library.models import Library
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, View

# Create your views here.
class SongViewController(APIView):
    def get(self, request):
        songs = Song.objects.all()
        serializer = SongSerializer(songs, many = True)
        return Response(serializer.data)

    def post(self, request):
        body = request.data
        serializer = SongSerializerSave(data=body)
        if serializer.is_valid():
            serializer.save() # INSERT 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk) :
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

    def delete(self, request, pk):
        try:
            song = Song.objects.get(pk=pk)
        except Song.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        song.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CreateSongView(CreateView):
    def get(self, request):
        prompts = Prompt.objects.all()
        libraries = Library.objects.all()
        return render(request, "song/create-song.html", {"prompts": prompts, "libraries": libraries})
    def post(self, request):
        form = SongForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Song created successfully")
            return redirect("create_song_template")

class SearchSongView(ListView):
    def get(self, request):
        song_name = request.GET.get("song_name")
        if song_name == None or song_name == "":
            songs = Song.objects.all()
        else:
            songs = Song.objects.filter(song_name__contains=song_name)
            
        return render(request, "song/search-song.html", {"songs": songs} )

class DeleteSongView(DeleteView):
    def get(self, request):
        pk = request.GET.get("id")
        try:
            song = Song.objects.get(pk=pk)
            song.delete()
            messages.success(request, "Song deleted successfully")
            
        except Song.DoesNotExist:
            print(f"Song id:{pk} does not exist")
            messages.error(request, "Song cannot be deleted because this song does not exist")
            
        return redirect("search_song")

class UpdateSongView(UpdateView):
    def get(self, request):
        pk = request.GET.get("id")
        old_song = get_object_or_404(Song, id=pk)
        prompts = Prompt.objects.all()
        libraries = Library.objects.all()
        return render(request, "song/update-song.html", {"song": old_song, "prompts": prompts, "libraries": libraries})

    def post(self, request):
        pk = request.GET.get("id")
        old_song = get_object_or_404(Song, id=pk)
        form = SongForm(request.POST, instance=old_song)
        if form.is_valid():
            form.save()
            messages.success(request, "Song updated successfully")
            return redirect("search_song")
        else:
            messages.error(request, "Song the input information was not complete")
            return redirect("search_song")
        
class SongView(View):
    def get(self, request):
        return render(request, "song/song.html")