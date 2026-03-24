from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Library
from .serializers import LibrarySerializer, LibrarySerializerSave
from django.shortcuts import render, redirect
from .forms import LibraryForm
from django.contrib import messages
from user.models import User

# Create your views here.
@api_view(["GET"])
def get_library(request):
    libraries = Library.objects.all()
    serializer = LibrarySerializer(libraries, many = True)
    return Response(serializer.data)

@api_view(["POST"])
def create_library(request):
    body = request.data
    serializer = LibrarySerializerSave(data=body)
    if serializer.is_valid():
        serializer.save() # INSERT 
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["PUT"])
def update_library(request, pk) :
    body = request.data
    try:
        library = Library.objects.get(pk=pk)
    except Library.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = LibrarySerializerSave(library, data=body)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def delete_library(request, pk):
    try:
        library = Library.objects.get(pk=pk)
    except Library.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    library.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

def create_library_template(request):
    # check if request from submit form
    if request.method == "POST":
        form = LibraryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Library created successfully")
            return redirect("create_library_template")
            
    # GET
    users = User.objects.all()
    return render(request, "library/create-library.html", {"users": users})

def search_library_template(request):
    username = request.GET.get("username")
    if username == None or username == "":
        libraries = Library.objects.all()
    else:
        libraries = Library.objects.filter(user__username__contains=username)
        
    return render(request, "library/search-library.html", {"libraries": libraries})

