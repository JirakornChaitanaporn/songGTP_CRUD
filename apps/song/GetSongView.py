from .models import Song, Status
from django.shortcuts import render, get_object_or_404
from apps.library.models import Library
from django.views.generic import View

class GetSongView(View):
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
            "prev_id": prev_id,
            "base_url": request.build_absolute_uri('/')
        })