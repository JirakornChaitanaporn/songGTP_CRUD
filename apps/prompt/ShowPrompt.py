from .models import Prompt
from django.shortcuts import render
from django.views.generic import  View

class ShowPrompt(View):
    def get(self, request):
        prompt = Prompt.objects.all()
        return render(request, "prompt/prompt_table.html", {"prompt":prompt})