from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer
from .forms import UserForm


# Create your views here.
class UserViewController(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many = True)
        return Response(serializer.data)

    def post(self, request):
        body = request.data
        serializer = UserSerializer(data=body)
        if serializer.is_valid():
            serializer.save() # INSERT 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk) :
        body = request.data
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserSerializer(user, data=body)
        if serializer.is_valid():
            serializer.save() # UPDATE
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#need to create library at the same time
class CreateUserView(CreateView):
    def get(self, request):
        return render(request, "user/create-user.html")
    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully") # messages = []
            return redirect("create_user_template")

class SearchUserView(ListView):
    def get(self, request):
        username = request.GET.get("username")
        if username == None or username == "":
            users = User.objects.all()
        else:
            users = User.objects.filter(username__contains=username)
            
        return render(request, "user/search-user.html", {"users": users} )

class DeleteUserView(DeleteView):
    def get(self, request):
        pk = request.GET.get("id")
        try:
            users = User.objects.get(pk=pk)
            users.delete()
            messages.success(request, "User deleted successfully")
            
        except User.DoesNotExist:
            print(f"User id:{pk} does not exist")
            messages.error(request,"User cannot be deleted because this user does not exist")
            
        return redirect("search_user")

# class UpdateUserView(UpdateView):
#     def get(self, request):
#         pk = request.GET.get("id")
#         old_user = get_object_or_404(User, id=pk)
#         return render(request, "user/update-user.html", {"user": old_user})

#     def post(self, request):
#         pk = request.GET.get("id")
#         old_user = get_object_or_404(User, id=pk)

#         form = UserForm(request.POST, instance=old_user)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "User updated successfully") # messages = []
#             return redirect("search_user")
#         else:
#             messages.error(request, "User the input information was not complete") # messages = []
#             return redirect("search_user")
