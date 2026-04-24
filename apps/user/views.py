# from django.shortcuts import get_object_or_404, render, redirect
# from django.contrib import messages
# from django.contrib.auth import logout as auth_logout
# from django.views.generic import ListView, CreateView, DeleteView, UpdateView, View
# from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator
# from rest_framework.decorators import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import User
# from .serializers import UserSerializer
# from .forms import UserForm
# from django.conf import settings


# # Create your views here.
# class GoogleOAuthRedirectView(View):
#     """Redirect to allauth's Google login — allauth handles the OAuth flow correctly."""
#     def get(self, request):
#         next_url = request.GET.get("next")
#         if next_url:
#             return redirect(f'/accounts/google/login/?next={next_url}')
#         else:
#             return redirect(f'/accounts/google/login/')
    
# class UserLoginView(View):
#     """Handle user sign-in (login) with Google OAuth and traditional login"""
#     def get(self, request):
#         if request.user.is_authenticated:
#             return redirect('/library/')
#         return render(request, "user/sign-in.html")
    
#     def post(self, request):
#         # Handle traditional login if form is submitted
#         username = request.POST.get('username')
#         password = request.POST.get('password')
        
#         if username and password:
#             from django.contrib.auth import authenticate, login
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 messages.success(request, f"Welcome back, {user.username}!")
#                 return redirect("library")
#             else:
#                 messages.error(request, "Invalid username or password")
        
#         return render(request, "user/sign-in.html")


# class LogoutView(View):
#     """Handle user logout"""
#     def get(self, request):
#         auth_logout(request)
#         return redirect("login")
    
#     def post(self, request):
#         auth_logout(request)
#         return redirect("login")
