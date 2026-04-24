import abc

class Factory:
    def __init__(self, chosen_strat):
        self.__chosen_strat = chosen_strat
    
    def use_strat(self):
        if self.__chosen_strat == "MOCK":
            return MockSongGeneratorStrategy()
        else:
            return SunoSongGeneratorStrategy()

class StratTemplate(abc.ABC):
    def __init__(self):
        raise NotImplementedError("please implement it")
    
    # def generate_song(self, request):
    #     raise NotImplementedError("Please implement generating song")
    
    def generate(self):
        raise NotImplementedError("Please implement generate")
    
import os
from apps.prompt.forms import PromptForm
from django.contrib import messages
import requests as req
from random import randint
from apps.song.models import Song, Status
from apps.prompt.models import Generation
from apps.library.models import Library
from django.shortcuts import render, redirect

class MockSongGeneratorStrategy(StratTemplate):
    def __init__(self, song_name, song_genre, song_mood, generation_status, description, lyrics, keywords):
        self.song_name = song_name
        self.song_genre = song_genre
        self.song_mood = song_mood
        self.generation_status = generation_status
        self.description = description
        self.lyrics = lyrics
        self.keywords = keywords
        
    def generate(self, request):
        form = PromptForm(request.POST)
        if form.is_valid():
            # form.cleaned_data["task_id"] = "mock" + str(randint(1,69))
            # form.cleaned_data["generation_status"] = "generating"
            prompt_instance = form.save(commit=False)
            prompt_instance.task_id = "mock" + str(randint(1,69))
            prompt_instance.generation_status = Generation.SUCCESS
            prompt_instance.user = request.user
            prompt_instance.save()
            messages.success(request, "Prompt created successfully please go to library to see the mock result") # messages = []
            
            user_id = request.user.id
            library = Library.objects.filter(user=user_id)
            if len(library) > 0:
                song = Song.objects.create(
                    prompt = prompt_instance,
                    library = library[0],
                    song_name = prompt_instance.song_name,
                    image_link= "https://cdn.pixabay.com/photo/2015/10/25/22/00/minecraft-1006433_1280.jpg",
                    song_url="https://tempfile.aiquickdraw.com/r/e2ab2013260f4a239da4f783cfca0630.mp3",
                    shared_code=f"localhost:8000/song/id",
                    sharing_status=Status.PRIVATE,
                    description="Get rickrolled",
                    lyrics="There no stranger to loves you know the rule and so do I",
                    length="3.30"
                )
                song.shared_code = f"localhost:8000/song/{song.id}"
                song.save()
                return redirect("create_prompt_mockup")
            else:
                messages.error(request, "library does not exist")
                return redirect("create_prompt_mockup")
        else:
            messages.error(request, "Generating error") # messages = []
            return redirect("create_prompt_mockup")

class SunoSongGeneratorStrategy(StratTemplate):
    def __init__(self, song_name, song_genre, song_mood, generation_status, description, lyrics, keywords):
        self.song_name = song_name
        self.song_genre = song_genre
        self.song_mood = song_mood
        self.generation_status = generation_status
        self.description = description
        self.lyrics = lyrics
        self.keywords = keywords
        
    def generate(self):
        suno_key = os.getenv("SUNO_API_KEY")
        if self.lyrics == "" or self.lyrics == None:
            params = {
                "customMode": True,
                "Instrumental": False,
                "model":"V4",
                "callBackUrl": "https://api.example.com/callback",
                "prompt": f"Mood: {self.song_mood} | Keyword contain: {self.keywords} | Song description: {self.description} | Duration 2to3 minutes",
                "style": f"{self.song_genre}",
                "title":f"{self.song_name}",
                "negativeTags": "Swearing like 'f*ck off racism illegal and political drama'",
            }
        else:
            params = {
                "customMode": True,
                "Instrumental": False,
                "model":"V4",
                "callBackUrl": "https://api.example.com/callback",
                "prompt": f"{self.lyrics}",
                "style": f"{self.song_genre}",
                "title": f"{self.song_name}",
                "negativeTags": "Swearing like 'f*ck off racism illegal and political drama'",
            }

        headers = {
            "Authorization": f"Bearer {suno_key}",
            "Content-Type": "application/json"
        }

        resp = req.post("https://api.sunoapi.org/api/v1/generate", json=params, headers=headers)
        # status = req.get("https://api.sunoapi.org/api/v1/generate/record-info", headers={"Authorization": f"Bearer {suno_key}"})
        
        return resp
    
