from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer
from .forms import UserForm
from django.conf import settings


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
class CreateUserView(View):
    """Handle user sign-up with traditional form"""
    def get(self, request):
        return render(request, "user/create-user.html")
    
    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully")
            return redirect("login")
        else:
            messages.error(request, "Error creating user. Please check your information.")
            return render(request, "user/create-user.html", {"form": form})

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

class GoogleOAuthRedirectView(View):
    """Redirect to allauth's Google login — allauth handles the OAuth flow correctly."""
    def get(self, request):
        return redirect('/accounts/google/login/')
    
class UserLoginView(View):
    """Handle user sign-in (login) with Google OAuth and traditional login"""
    def get(self, request):
        return render(request, "user/sign-in.html")
    
    def post(self, request):
        # Handle traditional login if form is submitted
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            from django.contrib.auth import authenticate, login
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password")
        
        return render(request, "user/sign-in.html")


class LogoutView(View):
    """Handle user logout"""
    def get(self, request):
        auth_logout(request)
        messages.success(request, "You have been logged out successfully")
        return redirect("login")
    
    def post(self, request):
        auth_logout(request)
        messages.success(request, "You have been logged out successfully")
        return redirect("login")


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
