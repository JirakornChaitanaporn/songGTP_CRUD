import hashlib
from random import randint

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
