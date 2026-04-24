from .models import Song, Status
from django.shortcuts import render
from django.views.generic import View


class GetPublicSongView(View):
    def get(self, request):
        from django.core.exceptions import PermissionDenied
        # Only show the song if it exists AND its status is PUBLIC
        shared_code = request.GET.get('shared_code')
        song = Song.objects.filter(shared_code=shared_code)
        print(shared_code)
        print(song[0].id)
        print(song[0].sharing_status)
        if song[0].sharing_status != Status.PUBLIC:
            raise PermissionDenied("This song is not public.")
        
        return render(request, "song/song_public.html", {
            "song": song[0],
        })
