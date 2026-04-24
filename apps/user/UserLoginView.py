from django.views.generic import View
from django.shortcuts import render, redirect


class UserLoginView(View):
    """Handle user sign-in (login) with Google OAuth and traditional login"""
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/library/')
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
                return redirect("library")
        
        return render(request, "user/sign-in.html")