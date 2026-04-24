from django.views.generic import View
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect

class LogoutView(View):
    """Handle user logout"""
    def get(self, request):
        auth_logout(request)
        return redirect("login")
    
    def post(self, request):
        auth_logout(request)
        return redirect("login")
