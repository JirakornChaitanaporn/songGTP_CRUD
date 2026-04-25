from .models import Prompt, Generation
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.test import APIRequestFactory
from django.db.models import Q
from apps.prompt.SunoStatusViewController import SunoStatusViewController

class ShowPrompt(LoginRequiredMixin, View):
    login_url = "/login/"
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("login")
        user_id = request.user.id
        
        # Check status for unfinished prompts
        unfinished_prompts = Prompt.objects.filter(Q(generation_status=Generation.PENDING) & Q(user=user_id))
        factory = APIRequestFactory()
        status_view = SunoStatusViewController.as_view()
        
        for p in unfinished_prompts:
            if p.task_id:
                api_request = factory.get(f"api/suno-status/")
                status_resp = status_view(api_request, tid=p.task_id, uid=user_id)
                
        prompt = Prompt.objects.filter(user=user_id).order_by('-created_at')
        return render(request, "prompt/prompt_table.html", {"prompt":prompt})