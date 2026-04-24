from .models import Song, Status
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import View

class PatchSharingStatusView(View):
    def post(self, request, pk):
        song = get_object_or_404(Song, pk=pk)

        # Trace ownership: Song → library (FK) → user (OneToOne) → id
        # Only the owner of this song's library can change sharing status
        song_owner_id = song.library.user.id

        if not request.user.is_authenticated or request.user.id != song_owner_id:
            # Not the owner — do nothing, silently redirect back
            return redirect('song', pk=song.id)

        # change status
        if song.sharing_status == Status.PUBLIC:
            song.sharing_status = Status.PRIVATE
        else:
            song.sharing_status = Status.PUBLIC
        song.save()

        # Redirect back to the song page
        return redirect('song', pk=song.id)