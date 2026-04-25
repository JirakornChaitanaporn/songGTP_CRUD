import os
import requests as req

from django.contrib import messages
from django.shortcuts import redirect

from apps.prompt.forms import PromptForm
from apps.prompt.models import Generation
from apps.prompt.StrategyTemplate import SongGenerationStrategy

class SunoSongGeneratorStrategy(SongGenerationStrategy):
    """
    Calls the real Suno API to generate an actual song.
    Requires SUNO_API_KEY to be set in .env
    Selected when STRAT_CHOSEN=REAL in .env
    """

    def generate(self, request):
        """
        generate(request) -> HttpResponse

        Validates the PromptForm, builds the Suno API payload,
        saves the prompt with a taskId, and redirects.
        """
        suno_key = os.getenv("SUNO_API_KEY")
        form = PromptForm(request.POST)

        if form.is_valid():
            lyrics = form.cleaned_data.get("lyrics")

            # Auto-mode: no lyrics provided — let Suno write them
            if not lyrics:
                params = {
                    "customMode": False,
                    "Instrumental": False,
                    "model": "V4",
                    "callBackUrl": "https://api.example.com/callback",
                    "prompt": (
                        f"Mood: {form.cleaned_data['song_mood']} | "
                        f"Keyword contain: [{form.cleaned_data['keywords']}] "
                        f"(you can add more words to make the song more meaningful) | "
                        f"Song description: {form.cleaned_data['description']} | "
                        f"Duration 2 to 3 minutes"
                    ),
                    "style": form.cleaned_data["song_genre"],
                    "title": form.cleaned_data["song_name"],
                    "negativeTags": "Swearing like 'f*ck off', racism, illegal and political drama",
                }
            # Custom-mode: user provided lyrics
            else:
                params = {
                    "customMode": True,
                    "Instrumental": False,
                    "model": "V4",
                    "callBackUrl": "https://api.example.com/callback",
                    "prompt": lyrics,
                    "style": form.cleaned_data["song_genre"],
                    "title": form.cleaned_data["song_name"],
                    "negativeTags": "Swearing like 'f*ck off', racism, illegal and political drama",
                }

            headers = {
                "Authorization": f"Bearer {suno_key}",
                "Content-Type": "application/json",
            }

            resp = req.post(
                "https://api.sunoapi.org/api/v1/generate",
                json=params,
                headers=headers,
            )
            json_resp = resp.json()

            if resp.status_code == 200:
                prompt_instance = form.save(commit=False)
                prompt_instance.generation_status = Generation.PENDING
                prompt_instance.task_id = json_resp["data"]["taskId"]
                prompt_instance.user = request.user
                prompt_instance.save()

                messages.success(
                    request,
                    "Prompt created successfully — go to your library to check generation status.",
                )
                return redirect("generate_song")
            else:
                prompt_instance = form.save(commit=False)
                prompt_instance.generation_status = Generation.ERROR
                prompt_instance.save()

                messages.error(request, "Suno API error — could not generate song.")
                return redirect("generate_song")
        else:
            messages.error(request, "Form validation failed. Please check your inputs.")
            return redirect("generate_song")
