# from rest_framework.test import APIRequestFactory
# from django.db.models import Q

# from .models import Library
# from django.shortcuts import render, redirect 
# from apps.song.models import Song
# from apps.prompt.models import Prompt, Generation
# from apps.prompt.SunoStatusViewController import SunoStatusViewController
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.views.generic import View

# # Create your views here.
# class LibraryView(LoginRequiredMixin, View):
#     login_url = "/login/"
#     def get(self, request):
#         if not request.user.is_authenticated:
#             return redirect("login")
#         user_id = request.user.id
#         # Get x
#         unfinished_prompts = Prompt.objects.filter(Q(generation_status=Generation.PENDING) & Q(user=user_id))
#         factory = APIRequestFactory()
#         status_view = SunoStatusViewController.as_view()
        
#         for prompt in unfinished_prompts:
#             tid = prompt.task_id
#             api_request = factory.get(f"api/suno-status/")
#             status_resp = status_view(api_request, tid=tid, uid=user_id)
            
        
#         library = Library.objects.filter(user=user_id).first()
#         if not library:
#             return render(request, "library/library.html", {"song_list": []})
#         songs = Song.objects.filter(library=library)
#         return render(request, "library/library.html", {"song_list":songs})