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
import requests
from django.http import StreamingHttpResponse, Http404, HttpResponse

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
            
        return redirect("library")

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
    def get(self, request, pk):
        from django.core.exceptions import PermissionDenied
        from django.contrib.auth.views import redirect_to_login
        
        song = get_object_or_404(Song, pk=pk)
        
        if song.sharing_status != Status.PUBLIC:
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path())
            elif song.library.user != request.user:
                raise PermissionDenied("You do not have access to this private song.")
        
        # Get all songs from all libraries belonging to the user for navigation
        if request.user.is_authenticated and song.library.user == request.user:
            user_libraries = Library.objects.filter(user=request.user)
            library_songs = Song.objects.filter(library__in=user_libraries).distinct().order_by('id')
            
            # Find next song in the same library (with looping)
            next_songs = library_songs.filter(id__gt=song.id)
            if next_songs.exists():
                next_song = next_songs.first()
            else:
                # Loop back to the first song in the library
                next_song = library_songs.first()
            
            next_id = next_song.id if next_song else None
            
            # Find previous song in the same library (with looping)
            prev_songs = library_songs.filter(id__lt=song.id).order_by('-id')
            if prev_songs.exists():
                prev_song = prev_songs.first()
            else:
                # Loop back to the last song in the library
                prev_song = library_songs.last()
            
            prev_id = prev_song.id if prev_song else None
        else:
            next_id = None
            prev_id = None
            
        return render(request, "song/song.html", {
            "song": song,
            "next_id": next_id,
            "prev_id": prev_id
        })

class DownloadSongView(View):
    def get(self, request, pk):
        from django.core.exceptions import PermissionDenied
        song = get_object_or_404(Song, pk=pk)
        
        # Access control: check if public or if user is owner
        if song.sharing_status != Status.PUBLIC:
            if not request.user.is_authenticated:
                return redirect('login')
            elif song.library.user != request.user:
                raise PermissionDenied("You do not have access to download this private song.")

        if not song.song_url:
            raise Http404("Song URL not found")
        
        try:
            response = requests.get(song.song_url, stream=True)
            response.raise_for_status()
            
            filename = f"{song.song_name}.mp3".replace(" ", "_")
            content_type = response.headers.get('content-type', 'audio/mpeg')
            
            django_response = StreamingHttpResponse(
                response.iter_content(chunk_size=8192),
                content_type=content_type
            )
            django_response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return django_response
        except Exception as e:
            return HttpResponse(f"Error downloading file: {str(e)}", status=500)