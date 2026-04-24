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
import os

# Create your views here.

# class DeleteSongView(DeleteView):
#     def get(self, request):
#         pk = request.GET.get("id")
#         try:
#             song = Song.objects.get(pk=pk)
#             prompt = Prompt.objects.get(pk=song.prompt.id)
#             prompt.delete()
#             song.delete()
#             messages.success(request, "Song deleted successfully")
            
#         except Song.DoesNotExist:
#             print(f"Song id:{pk} does not exist")
#             messages.error(request, "Song cannot be deleted because this song does not exist")
            
#         return redirect("library")
        
# class SongView(View):
#     def get(self, request, pk):
#         from django.core.exceptions import PermissionDenied
#         from django.contrib.auth.views import redirect_to_login
        
#         song = get_object_or_404(Song, pk=pk)
        
#         if song.sharing_status != Status.PUBLIC:
#             if not request.user.is_authenticated:
#                 return redirect_to_login(request.get_full_path())
#             elif song.library.user != request.user:
#                 raise PermissionDenied("You do not have access to this private song.")
        
#         # Get all songs from all libraries belonging to the user for navigation
#         if request.user.is_authenticated and song.library.user == request.user:
#             user_libraries = Library.objects.filter(user=request.user)
#             library_songs = Song.objects.filter(library__in=user_libraries).distinct().order_by('id')
            
#             # Find next song in the same library (with looping)
#             next_songs = library_songs.filter(id__gt=song.id)
#             if next_songs.exists():
#                 next_song = next_songs.first()
#             else:
#                 # Loop back to the first song in the library
#                 next_song = library_songs.first()
            
#             next_id = next_song.id if next_song else None
            
#             # Find previous song in the same library (with looping)
#             prev_songs = library_songs.filter(id__lt=song.id).order_by('-id')
#             if prev_songs.exists():
#                 prev_song = prev_songs.first()
#             else:
#                 # Loop back to the last song in the library
#                 prev_song = library_songs.last()
            
#             prev_id = prev_song.id if prev_song else None
#         else:
#             next_id = None
#             prev_id = None
            
#         return render(request, "song/song.html", {
#             "song": song,
#             "next_id": next_id,
#             "prev_id": prev_id,
#             "base_url": os.getenv("BASE_URL")
#         })


# class PatchSharingStatusView(View):
#     def post(self, request, pk):
#         song = get_object_or_404(Song, pk=pk)

#         # Trace ownership: Song → library (FK) → user (OneToOne) → id
#         # Only the owner of this song's library can change sharing status
#         song_owner_id = song.library.user.id

#         if not request.user.is_authenticated or request.user.id != song_owner_id:
#             # Not the owner — do nothing, silently redirect back
#             return redirect('song', pk=song.id)

#         # change status
#         if song.sharing_status == Status.PUBLIC:
#             song.sharing_status = Status.PRIVATE
#         else:
#             song.sharing_status = Status.PUBLIC
#         song.save()

#         # Redirect back to the song page
#         return redirect('song', pk=song.id)


# class PublicSongView(View):
#     def get(self, request):
#         from django.core.exceptions import PermissionDenied
#         # Only show the song if it exists AND its status is PUBLIC
#         shared_code = request.GET.get('shared_code')
#         song = Song.objects.filter(shared_code=shared_code)
#         print(shared_code)
#         print(song[0].id)
#         print(song[0].sharing_status)
#         if song[0].sharing_status != Status.PUBLIC:
#             raise PermissionDenied("This song is not public.")
        
#         return render(request, "song/song_public.html", {
#             "song": song[0],
#         })

# class DownloadSongView(View):
#     def get(self, request, pk):
#         from django.core.exceptions import PermissionDenied
#         song = get_object_or_404(Song, pk=pk)
        
#         # Access control: check if public or if user is owner
#         if song.sharing_status != Status.PUBLIC:
#             if not request.user.is_authenticated:
#                 return redirect('login')
#             elif song.library.user != request.user:
#                 raise PermissionDenied("You do not have access to download this private song.")

#         if not song.song_url:
#             raise Http404("Song URL not found")
        
#         try:
#             response = requests.get(song.song_url, stream=True)
#             response.raise_for_status()
            
#             filename = f"{song.song_name}.mp3".replace(" ", "_")
#             content_type = response.headers.get('content-type', 'audio/mpeg')
            
#             django_response = StreamingHttpResponse(
#                 response.iter_content(chunk_size=8192),
#                 content_type=content_type
#             )
#             django_response['Content-Disposition'] = f'attachment; filename="{filename}"'
#             return django_response
#         except Exception as e:
#             return HttpResponse(f"Error downloading file: {str(e)}", status=500)