from .models import Generation
from django.shortcuts import render, redirect
from .forms import PromptForm
from django.views.generic import View
from django.contrib import messages
import os
import requests as req

class CreateGenerateSongView(View):
    def get(self, request):
        return render(request, "prompt/generate_song.html")

    def post(self, request):
        suno_key = os.getenv("SUNO_API_KEY")
        form = PromptForm(request.POST)
        if form.is_valid(): 
            if form.cleaned_data["lyrics"] == "" or form.cleaned_data["lyrics"] == None:
                params = {
                    "customMode": False,
                    "Instrumental": False,
                    "model":"V4",
                    "callBackUrl": "https://api.example.com/callback",
                    "prompt": f"Mood: {form.cleaned_data["song_mood"]} | Keyword contain: [{form.cleaned_data["keywords"]}] (you can add more word than this to make the song more meaningful) | Song description: {form.cleaned_data["description"]} | Duration 2to3 minutes",
                    "style": f"{form.cleaned_data["song_genre"]}",
                    "title":f"{form.cleaned_data["song_name"]}",
                    "negativeTags": "Swaering like 'f*ck off'",
                }
            else:
                params = {
                    "customMode": True,
                    "Instrumental": False,
                    "model":"V4",
                    "callBackUrl": "https://api.example.com/callback",
                    "prompt": f"{form.cleaned_data["lyrics"]}",
                    "style": f"{form.cleaned_data["song_genre"]}",
                    "title": f"{form.cleaned_data["song_name"]}",
                    "negativeTags": "Swaering like 'f*ck off'",
                }

            headers = {
                "Authorization": f"Bearer {suno_key}",
                "Content-Type": "application/json"
            }

            resp = req.post("https://api.sunoapi.org/api/v1/generate", json=params, headers=headers)
            # status = req.get("https://api.sunoapi.org/api/v1/generate/record-info", headers={"Authorization": f"Bearer {suno_key}"})
            json = resp.json()
            if resp.status_code == 200:
                print(resp.json())
                prompt_instance = form.save(commit=False)
                prompt_instance.generation_status = Generation.PENDING
                prompt_instance.task_id = json["data"]["taskId"]
                prompt_instance.user = request.user
                prompt_instance.save()
                messages.success(request, "Prompt created successfully please go to library to check the result and generating status") # messages = []
                return redirect("generate_song")
            else:
                prompt_instance = form.save(commit=False)
                prompt_instance.generation_status = Generation.ERROR
                prompt_instance.save()
                messages.error(request, "Generating error") # messages = []
                return redirect("generate_song")
        else:
            messages.error(request, "Form validation failed. Please check the inputs.")
            return render(request, "prompt/generate_song.html", {"form": form})