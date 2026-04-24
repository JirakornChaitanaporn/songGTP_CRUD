from django.views.generic import DeleteView
from apps.song.models import Song
from django.shortcuts import redirect
from django.contrib import messages
from apps.prompt.models import Prompt

class DeleteSongView(DeleteView):
    def get(self, request):
        pk = request.GET.get("id")
        try:
            song = Song.objects.get(pk=pk)
            prompt = Prompt.objects.get(pk=song.prompt.id)
            prompt.delete()
            song.delete()
            messages.success(request, "Song deleted successfully")
            
        except Song.DoesNotExist:
            print(f"Song id:{pk} does not exist")
            messages.error(request, "Song cannot be deleted because this song does not exist")
            
        return redirect("library")