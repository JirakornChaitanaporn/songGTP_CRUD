from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Library
from .serializers import LibrarySerializer, LibrarySerializerSave
from django.shortcuts import render, redirect , get_object_or_404
from .forms import LibraryForm
from apps.song.models import Song
from django.contrib import messages
from apps.user.models import User
from django.views.generic import ListView, CreateView, DeleteView, UpdateView , View

# Create your views here.
class LibraryViewController(APIView):
    def get(self, request):
        libraries = Library.objects.all()
        serializer = LibrarySerializer(libraries, many = True)
        return Response(serializer.data)

    def post(self, request):
        body = request.data
        serializer = LibrarySerializerSave(data=body)
        if serializer.is_valid():
            serializer.save() # INSERT 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk) :
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

    def delete(self, request, pk):
        try:
            library = Library.objects.get(pk=pk)
        except Library.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        library.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CreateLibraryView(CreateView):
    def get(self, request):
        users = User.objects.all()
        return render(request, "library/create-library.html", {"users": users})
    def post(self, request):
        form = LibraryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Library created successfully")
            return redirect("create_library_template")

class SearchLibraryView(ListView):
    def get(self, request):
        username = request.GET.get("username")
        if username == None or username == "":
            libraries = Library.objects.all()
        else:
            libraries = Library.objects.filter(user__username__contains=username)
            
        return render(request, "library/search-library.html", {"libraries": libraries})

class DeleteLibraryView(DeleteView):
    def get(self, request):
        pk = request.GET.get("id")
        try:
            libraries = Library.objects.get(pk=pk)
            libraries.delete()
            messages.success(request, "Library deleted successfully")
            
        except Library.DoesNotExist:
            print(f"Library id:{pk} does not exist")
            messages.error(request,"Library cannot be deleted because this library does not exist")
            
        return redirect("search_library")

class UpdateLibraryView(UpdateView):
    def get(self, request):
        pk = request.GET.get("id")
        old_library = get_object_or_404(Library, id=pk)
        users = User.objects.all()
        return render(request, "library/update-library.html", {"library": old_library, "users": users})

    def post(self, request):
        pk = request.GET.get("id")
        old_library = get_object_or_404(Library, id=pk)
        form = LibraryForm(request.POST, instance=old_library)
        if form.is_valid():
            form.save()
            messages.success(request, "Library updated successfully") # messages = []
            return redirect("search_library")
        else:
            messages.error(request, "Library the input information was not complete") # messages = []
            return redirect("search_library")
        
class LibraryView(View):
    def get(self, request):
        user_id = request.user.id
        library = Library.objects.filter(user=user_id).first()
        if not library:
            return render(request, "library/library.html", {"song_list": []})
        songs = Song.objects.filter(library=library)
        return render(request, "library/library.html", {"song_list":songs})