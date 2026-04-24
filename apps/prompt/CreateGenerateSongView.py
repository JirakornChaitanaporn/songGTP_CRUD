from django.shortcuts import render
from django.views.generic import View

from apps.prompt.Context import SongGenerationContext


class CreateGenerateSongView(View):
    """
    View for the real song generation form.

    GET  — renders the generate_song.html template.
    POST — delegates song generation entirely to SongGenerationContext,
           which reads STRAT_CHOSEN from .env and runs the correct strategy.
    """

    def get(self, request):
        return render(request, "prompt/generate_song.html")

    def post(self, request):
        context = SongGenerationContext()
        return context.execute(request)