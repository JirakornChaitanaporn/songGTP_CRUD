from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Prompt, Generation
from apps.song.models import Song
from apps.song.models import Status
from apps.library.models import Library
from apps.song.serializers import SongSerializerSave
from .serializers import PromptSerializer
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PromptForm
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, View
from django.contrib import messages
import os
import requests as req
from random import randint

# from strategy import MockSongGeneratorStrategy, SunoSongGeneratorStrategy

# Create your views here.
class PromptViewController(APIView):
    def get(self, request):
        prompts = Prompt.objects.all()
        serializer = PromptSerializer(prompts, many = True)
        return Response(serializer.data)

    def post(self, request):
        body = request.data
        serializer = PromptSerializer(data=body)
        if serializer.is_valid():
            serializer.save() # INSERT 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk) :
        body = request.data
        try:
            prompt = Prompt.objects.get(pk=pk)
        except Prompt.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = PromptSerializer(prompt, data=body)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            prompt = Prompt.objects.get(pk=pk)
        except Prompt.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        prompt.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SunoStatusViewController(APIView):
    def get(self, request, tid, lid):
        suno_key = os.getenv("SUNO_API_KEY")
        resp = req.get(f"https://api.sunoapi.org/api/v1/generate/record-info?taskId={tid}", headers={"Authorization": f"Bearer {suno_key}"})
        json = resp.json()
        if json["code"] == 200:
            # update prompt
            try:
                lastest_prompt = Prompt.objects.filter(task_id=tid)
                if json["data"]["status"] == "SUCCESS":
                    prompt_serializer = PromptSerializer(lastest_prompt[0], data={"generation_status": Generation.SUCCESS}, partial=True)
                    if prompt_serializer.is_valid():
                        saved_prompt = prompt_serializer.save()
                        song_serializer = SongSerializerSave(data = {
                            "prompt": saved_prompt.id,
                            "library": lid,
                            "song_name": json["data"]["response"]["sunoData"][0]["title"],
                            "song_url": json["data"]["response"]["sunoData"][0]["audioUrl"],
                            "shared_link": f"localhost:8000/song/1",
                            "sharing_status": Status.PRIVATE,
                            "description": saved_prompt.description,
                            "lyrics": saved_prompt.lyrics,
                            "length": json["data"]["response"]["sunoData"][0]["duration"]
                        })
                        if song_serializer.is_valid():
                            print("valid again")
                            song_serializer.save()
                        else:
                            print(song_serializer.errors)
            except Prompt.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            
            return Response(json, status=status.HTTP_200_OK)
        else:
            return Response(json, status=status.HTTP_400_BAD_REQUEST)
        
        


class CreatePromptView(CreateView):
    def get(self, request):
        return render(request, "prompt/create-prompt.html")
    def post(self, request):
        suno_key = os.getenv("SUNO_API_KEY")
        form = PromptForm(request.POST)
        if form.is_valid(): 
            if form.cleaned_data["lyrics"] == "" or form.cleaned_data["lyrics"] == None:
                params = {
                    "customMode": True,
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
            
            if resp.status_code == 200:
                print(resp.json())
                form.cleaned_data["generation_status"] = "generating"
                form.save()
                messages.success(request, "Prompt created successfully") # messages = []
                return redirect("create_prompt_template")
            else:
                form.cleaned_data["generation_status"] = "error"
                form.save()
                messages.error(request, "Generating error") # messages = []
                return redirect("create_prompt_template")

class CreatePromptMockupView(LoginRequiredMixin, CreateView):
    login_url = "/login/"
    def get(self, request):
        return render(request, "prompt/generate_song.html")
    
    def post(self, request):
        form = PromptForm(request.POST)
        if form.is_valid():
            # form.cleaned_data["task_id"] = "mock" + str(randint(1,69))
            # form.cleaned_data["generation_status"] = "generating"
            prompt_instance = form.save(commit=False)
            prompt_instance.task_id = "mock" + str(randint(1,69))
            prompt_instance.generation_status = Generation.SUCCESS
            prompt_instance.save()
            messages.success(request, "Prompt created successfully") # messages = []
            
            user_id = request.user.id
            library = Library.objects.filter(user=user_id)
            if len(library) > 0:
                song = Song.objects.create(
                    prompt = prompt_instance,
                    library = library[0],
                    song_name = prompt_instance.song_name,
                    image_link= "https://cdn.pixabay.com/photo/2015/10/25/22/00/minecraft-1006433_1280.jpg",
                    song_url="https://tempfile.aiquickdraw.com/r/e2ab2013260f4a239da4f783cfca0630.mp3",
                    shared_link="localhost:8000/id",
                    sharing_status=Status.PRIVATE,
                    description="Get rickrolled",
                    lyrics="There no stranger to loves you know the rule and so do I",
                    length="3.30"
                )
                song.save()
                return redirect("create_prompt_mockup")
            else:
                messages.error(request, "library does not exist")
                return redirect("create_prompt_mockup")
        else:
            messages.error(request, "Generating error") # messages = []
            return redirect("create_prompt_mockup")


class SearchPromptView(ListView):
    def get(self, request):
        song_name = request.GET.get("song_name")
        if song_name == None or song_name == "":
            prompts = Prompt.objects.all()
        else:
            prompts = Prompt.objects.filter(song_name__contains=song_name)
            
        return render(request, "prompt/search-prompt.html", {"prompts": prompts})

class DeletePromptView(DeleteView):
    def get(self, request):
        pk = request.GET.get("id")
        try:
            prompt = Prompt.objects.get(pk=pk)
            prompt.delete()
            messages.success(request, "Prompt deleted successfully")
            
        except Prompt.DoesNotExist:
            print(f"Prompt id:{pk} does not exist")
            messages.error(request, "Prompt cannot be deleted because this prompt does not exist")
            
        return redirect("search_prompt")

class UpdatePromptView(UpdateView):
    def get(self, request):
        pk = request.GET.get("id")
        old_prompt = get_object_or_404(Prompt, id=pk)
        return render(request, "prompt/update-prompt.html", {"prompt": old_prompt})

    def post(self, request):
        pk = request.GET.get("id")
        old_prompt = get_object_or_404(Prompt, id=pk)
        form = PromptForm(request.POST, instance=old_prompt)
        if form.is_valid():
            form.save()
            messages.success(request, "Prompt updated successfully")
            return redirect("search_prompt")
        else:
            messages.error(request, "Prompt the input information was not complete")
            return redirect("search_prompt")
        
class GenerateSongView(View):
    def get(self, request):
        return render(request, "prompt/generate_song.html")

    def post(self, request):
        suno_key = os.getenv("SUNO_API_KEY")
        form = PromptForm(request.POST)
        if form.is_valid(): 
            if form.cleaned_data["lyrics"] == "" or form.cleaned_data["lyrics"] == None:
                params = {
                    "customMode": True,
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
                prompt_instance.save()
                messages.success(request, "Prompt created successfully") # messages = []
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