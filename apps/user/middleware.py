from django.shortcuts import redirect
from django.urls import resolve, reverse

class LoginRequiredMiddleware:
    def __init__(self, get_respone):
        self.get_respone = get_respone
        self.allowed_path = [
            reverse('home'),
            reverse('login'),
            reverse('google_auth'),
            reverse('account_login'),
            reverse('account_logout'),
            reverse('account_signup'),
            "/accounts/google/login/",
            "/accounts/google/login/callback/",
            reverse('shared_song'),
            
        ]
        
    def __call__(self, request):
        
        path = request.path
        
        if not request.user.is_authenticated:
            #print(f"Not login any = {not any(url.startswith(path) for url in self.allowed_path)}")
            if not any(path.startswith(url) for url in self.allowed_path):
                return redirect(f"{reverse('login')}?next={path}")
        return self.get_respone(request)
        