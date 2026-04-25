import os
import hashlib
from random import randint

import requests as req
from django.contrib import messages
from django.shortcuts import redirect

from apps.prompt.forms import PromptForm
from apps.prompt.models import Generation
from apps.prompt.StrategyTemplate import SongGenerationStrategy
from apps.song.models import Song, Status
from apps.library.models import Library




class MockSongGeneratorStrategy(SongGenerationStrategy):
    """
    Generates a fake/placeholder song instantly.
    Does NOT call any external API — safe for local testing without a Suno key.
    Selected when STRAT_CHOSEN=MOCK in .env
    """

    def generate(self, request):
        """
        generate(request) -> HttpResponse

        Validates the PromptForm, saves a mock prompt + placeholder song,
        and redirects back to the mockup creation page.
        """
        form = PromptForm(request.POST)
        if form.is_valid():
            prompt_instance = form.save(commit=False)
            prompt_instance.task_id = "mock" + str(randint(1, 69))
            prompt_instance.generation_status = Generation.SUCCESS
            prompt_instance.user = request.user
            prompt_instance.save()

            messages.success(
                request,
                "Prompt created successfully — go to your library to see the mock result.",
            )

            library = Library.objects.filter(user=request.user.id)
            if library.exists():
                hash_code = hashlib.sha256(
                    f"prompt-{prompt_instance.id}".encode()
                ).hexdigest()[:12]

                song = Song.objects.create(
                    prompt=prompt_instance,
                    library=library[0],
                    song_name=prompt_instance.song_name,
                    image_link="https://cdn.pixabay.com/photo/2015/10/25/22/00/minecraft-1006433_1280.jpg",
                    song_url="https://tempfile.aiquickdraw.com/r/e2ab2013260f4a239da4f783cfca0630.mp3",
                    shared_code=hash_code,
                    sharing_status=Status.PRIVATE,
                    description="Just a mock song",
                    lyrics="Mock song",
                    length="210.0",
                )
                # Ensure the hash code is preserved as the shared_code
                song.save()

                return redirect("create_prompt_mockup")
            else:
                messages.error(request, "Library does not exist.")
                return redirect("create_prompt_mockup")
        else:
            messages.error(request, "Form validation failed — generating error.")
            return redirect("create_prompt_mockup")


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
