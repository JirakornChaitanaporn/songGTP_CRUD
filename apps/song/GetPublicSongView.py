from django.core.exceptions import PermissionDenied
from django.http import Http404
from .models import Song, Status
from django.shortcuts import render
from django.views.generic import View


class GetPublicSongView(View):
    def get(self, request):
        shared_code = request.GET.get('shared_code')
        song = Song.objects.filter(shared_code=shared_code).first()

        if song is None:
            raise Http404("Song not found.")

        if song.sharing_status != Status.PUBLIC:
            raise PermissionDenied("This song is not public.")

        return render(request, "song/song_public.html", {
            "song": song,
        })
