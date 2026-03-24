from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Prompt
from .serializers import PromptSerializer
from django.shortcuts import render, redirect
from .forms import PromptForm
from django.contrib import messages

@api_view(["GET"])
def get_prompt(request):
    prompts = Prompt.objects.all()
    serializer = PromptSerializer(prompts, many = True)
    return Response(serializer.data)

@api_view(["POST"])
def create_prompt(request):
    body = request.data
    serializer = PromptSerializer(data=body)
    if serializer.is_valid():
        serializer.save() # INSERT 
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["PUT"])
def update_prompt(request, pk) :
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


@api_view(["DELETE"])
def delete_prompt(request, pk):
    try:
        prompt = Prompt.objects.get(pk=pk)
    except Prompt.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    prompt.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

def create_prompt_template(request):
    # check if request from submit form
    if request.method == "POST":
        form = PromptForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Prompt created successfully")
            return redirect("create_prompt_template")
            
    # GET
    return render(request, "prompt/create-prompt.html")

def search_prompt_template(request):
    song_name = request.GET.get("song_name")
    if song_name == None or song_name == "":
        prompts = Prompt.objects.all()
    else:
        prompts = Prompt.objects.filter(song_name__contains=song_name)
        
    return render(request, "prompt/search-prompt.html", {"prompts": prompts})

