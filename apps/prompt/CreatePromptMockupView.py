from django.shortcuts import render
from django.views.generic import CreateView

from apps.prompt.Context import SongGenerationContext


class CreatePromptMockupView(CreateView):
    """
    View for the MOCK song generation form.

    GET  — renders generate_song.html
    POST — always uses MockSongGeneratorStrategy (no Suno API call)
    URL  — /create-prompt-mockup/
    """

    def get(self, request):
        return render(request, "prompt/generate_song.html")

    def post(self, request):
        # Always force MOCK strategy — no matter what .env says
        context = SongGenerationContext("mock")
        return context.execute(request)