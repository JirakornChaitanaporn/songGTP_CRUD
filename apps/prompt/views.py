from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Prompt
from .serializers import PromptSerializer
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PromptForm
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, View
from django.contrib import messages
import os
import requests as req
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
                    "prompt": f"Mood: {form.cleaned_data["song_mood"]} | Keyword contain: {form.cleaned_data["keywords"]} | Song description: {form.cleaned_data["description"]} | Duration 2to3 minutes",
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
        
class GeneratePromptView(View):
    def get(self, request):
        return render(request, "prompt/generate_song.html")
