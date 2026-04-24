from .models import Prompt, Generation
from apps.song.models import Song
from apps.song.models import Status
from apps.library.models import Library
from django.shortcuts import render, redirect
from .forms import PromptForm
from django.views.generic import CreateView, View
from django.contrib import messages
import os
import requests as req
from random import randint
import hashlib

# from strategy import MockSongGeneratorStrategy, SunoSongGeneratorStrategy

# Create your views here.

# class CreatePromptMockupView(CreateView):
#     def get(self, request):
#         return render(request, "prompt/generate_song.html")
    
#     def post(self, request):
#         form = PromptForm(request.POST)
#         if form.is_valid():
#             # form.cleaned_data["task_id"] = "mock" + str(randint(1,69))
#             # form.cleaned_data["generation_status"] = "generating"
#             prompt_instance = form.save(commit=False)
#             prompt_instance.task_id = "mock" + str(randint(1,69))
#             prompt_instance.generation_status = Generation.SUCCESS
#             prompt_instance.user = request.user
#             prompt_instance.save()
#             messages.success(request, "Prompt created successfully please go to library to see the mock result") # messages = []
            
#             user_id = request.user.id
#             library = Library.objects.filter(user=user_id)
#             if len(library) > 0:
#                 hash_code = hashlib.sha256(f"prompt-{prompt_instance.id}".encode()).hexdigest()[:12]
                
                
#                 song = Song.objects.create(
#                     prompt = prompt_instance,
#                     library = library[0],
#                     song_name = prompt_instance.song_name,
#                     image_link= "https://cdn.pixabay.com/photo/2015/10/25/22/00/minecraft-1006433_1280.jpg",
#                     song_url="https://tempfile.aiquickdraw.com/r/e2ab2013260f4a239da4f783cfca0630.mp3",
#                     shared_code=hash_code,
#                     sharing_status=Status.PRIVATE,
#                     description="Get rickrolled",
#                     lyrics="There no stranger to loves you know the rule and so do I",
#                     length="3.30"
#                 )
#                 song.save()
#                 return redirect("create_prompt_mockup")
#             else:
#                 messages.error(request, "library does not exist")
#                 return redirect("create_prompt_mockup")
#         else:
#             messages.error(request, "Generating error") # messages = []
#             return redirect("create_prompt_mockup")

# class ShowPrompt(View):
#     def get(self, request):
#         prompt = Prompt.objects.all()
#         return render(request, "prompt/prompt_table.html", {"prompt":prompt})

# class CreateGenerateSongView(View):
#     def get(self, request):
#         return render(request, "prompt/generate_song.html")

#     def post(self, request):
#         suno_key = os.getenv("SUNO_API_KEY")
#         form = PromptForm(request.POST)
#         if form.is_valid(): 
#             if form.cleaned_data["lyrics"] == "" or form.cleaned_data["lyrics"] == None:
#                 params = {
#                     "customMode": False,
#                     "Instrumental": False,
#                     "model":"V4",
#                     "callBackUrl": "https://api.example.com/callback",
#                     "prompt": f"Mood: {form.cleaned_data["song_mood"]} | Keyword contain: [{form.cleaned_data["keywords"]}] (you can add more word than this to make the song more meaningful) | Song description: {form.cleaned_data["description"]} | Duration 2to3 minutes",
#                     "style": f"{form.cleaned_data["song_genre"]}",
#                     "title":f"{form.cleaned_data["song_name"]}",
#                     "negativeTags": "Swaering like 'f*ck off'",
#                 }
#             else:
#                 params = {
#                     "customMode": True,
#                     "Instrumental": False,
#                     "model":"V4",
#                     "callBackUrl": "https://api.example.com/callback",
#                     "prompt": f"{form.cleaned_data["lyrics"]}",
#                     "style": f"{form.cleaned_data["song_genre"]}",
#                     "title": f"{form.cleaned_data["song_name"]}",
#                     "negativeTags": "Swaering like 'f*ck off'",
#                 }

#             headers = {
#                 "Authorization": f"Bearer {suno_key}",
#                 "Content-Type": "application/json"
#             }

#             resp = req.post("https://api.sunoapi.org/api/v1/generate", json=params, headers=headers)
#             # status = req.get("https://api.sunoapi.org/api/v1/generate/record-info", headers={"Authorization": f"Bearer {suno_key}"})
#             json = resp.json()
#             if resp.status_code == 200:
#                 print(resp.json())
#                 prompt_instance = form.save(commit=False)
#                 prompt_instance.generation_status = Generation.PENDING
#                 prompt_instance.task_id = json["data"]["taskId"]
#                 prompt_instance.user = request.user
#                 prompt_instance.save()
#                 messages.success(request, "Prompt created successfully please go to library to check the result and generating status") # messages = []
#                 return redirect("generate_song")
#             else:
#                 prompt_instance = form.save(commit=False)
#                 prompt_instance.generation_status = Generation.ERROR
#                 prompt_instance.save()
#                 messages.error(request, "Generating error") # messages = []
#                 return redirect("generate_song")
#         else:
#             messages.error(request, "Form validation failed. Please check the inputs.")
#             return render(request, "prompt/generate_song.html", {"form": form})