import abc

class StratTemplate(abc.ABC):
    def __init__(self):
        raise NotImplementedError("please implement it")
    
    # def generate_song(self, request):
    #     raise NotImplementedError("Please implement generating song")
    
    def send_json_to_suno(self):
        raise NotImplementedError("Please implement send_json_to_suno")
    
    def recieve_call_back(self, request):
        raise NotImplementedError("Please implement recieve_call_back")
    
import os
from apps.prompt.forms import PromptForm
from django.contrib import messages
import requests as req
class MockSongGeneratorStrategy(StratTemplate):
    def __init__(self, song_name, song_genre, song_mood, generation_status, description, lyrics, keywords):
        self.song_name = song_name
        self.song_genre = song_genre
        self.song_mood = song_mood
        self.generation_status = generation_status
        self.description = description
        self.lyrics = lyrics
        self.keywords = keywords
        
    def send_json_to_suno(self):
        resp = "okay"
        return resp
    
    def recieve_call_back(self, request):
        pass

class SunoSongGeneratorStrategy(StratTemplate):
    def __init__(self, song_name, song_genre, song_mood, generation_status, description, lyrics, keywords):
        self.song_name = song_name
        self.song_genre = song_genre
        self.song_mood = song_mood
        self.generation_status = generation_status
        self.description = description
        self.lyrics = lyrics
        self.keywords = keywords
        
    def send_json_to_suno(self):
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
    
    
    def recieve_call_back(self, request):
        pass

class ChooseStrategy:
    def __init__(self, chosen_strat):
        self.__chosen_strat = chosen_strat
    
    def use_strat(self):
        if self.__chosen_strat == "MOCK":
            return MockSongGeneratorStrategy()
        else:
            return SunoSongGeneratorStrategy()
