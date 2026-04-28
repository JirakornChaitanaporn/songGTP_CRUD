from django.shortcuts import render, redirect
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
        strategy, forced = SongGenerationContext.resolve("mock")
        # If .env locks a different strategy, redirect to the correct view
        if forced and strategy != "mock":
            return redirect("generate_song")
        return render(request, "prompt/generate_song.html", {
            "current_strategy": strategy,
            "strategy_forced": forced,
        })

    def post(self, request):
        strategy, forced = SongGenerationContext.resolve("mock")
        if forced and strategy != "mock":
            return redirect("generate_song")
        context = SongGenerationContext("mock")
        return context.execute(request)