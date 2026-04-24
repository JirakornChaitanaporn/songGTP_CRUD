from .models import Song, Status
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import View
import requests
from django.http import StreamingHttpResponse, Http404, HttpResponse


class GetDownloadSongView(View):
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