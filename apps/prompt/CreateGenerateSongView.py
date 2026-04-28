from django.shortcuts import render, redirect
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
        strategy, forced = SongGenerationContext.resolve("suno")
        # If .env locks a different strategy, redirect to the correct view
        if forced and strategy != "suno":
            return redirect("create_prompt_mockup")
        return render(request, "prompt/generate_song.html", {
            "current_strategy": strategy,
            "strategy_forced": forced,
        })

    def post(self, request):
        # Always force SUNO strategy — calls the real Suno API
        context = SongGenerationContext("suno")
        return context.execute(request)