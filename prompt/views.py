from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Prompt
from .serializers import PromptSerializer

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
