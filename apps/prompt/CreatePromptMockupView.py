from .models import Generation
from apps.song.models import Song
from apps.song.models import Status
from apps.library.models import Library
from django.shortcuts import render, redirect
from .forms import PromptForm
from django.views.generic import CreateView
from django.contrib import messages
from random import randint
import hashlib


class CreatePromptMockupView(CreateView):
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
            prompt_instance.user = request.user
            prompt_instance.save()
            messages.success(request, "Prompt created successfully please go to library to see the mock result") # messages = []
            
            user_id = request.user.id
            library = Library.objects.filter(user=user_id)
            if len(library) > 0:
                hash_code = hashlib.sha256(f"prompt-{prompt_instance.id}".encode()).hexdigest()[:12]
                
                
                song = Song.objects.create(
                    prompt = prompt_instance,
                    library = library[0],
                    song_name = prompt_instance.song_name,
                    image_link= "https://cdn.pixabay.com/photo/2015/10/25/22/00/minecraft-1006433_1280.jpg",
                    song_url="https://tempfile.aiquickdraw.com/r/e2ab2013260f4a239da4f783cfca0630.mp3",
                    shared_code=hash_code,
                    sharing_status=Status.PRIVATE,
                    description="Just a mock song",
                    lyrics="Mock song",
                    length="210.0"
                )
                song.save()
                return redirect("create_prompt_mockup")
            else:
                messages.error(request, "library does not exist")
                return redirect("create_prompt_mockup")
        else:
            messages.error(request, "Generating error") # messages = []
            return redirect("create_prompt_mockup")