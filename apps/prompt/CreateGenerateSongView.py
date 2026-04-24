from django.shortcuts import render
from django.views.generic import View

from apps.prompt.Context import SongGenerationContext


class CreateGenerateSongView(View):
    """
    View for the REAL (Suno) song generation form.

    GET  — renders generate_song.html
    POST — always uses SunoSongGeneratorStrategy (calls the real Suno API)
    URL  — /generate-song/
    """

    def get(self, request):
        return render(request, "prompt/generate_song.html")

    def post(self, request):
        # Always force SUNO strategy — calls the real Suno API
        context = SongGenerationContext("suno")
        return context.execute(request)