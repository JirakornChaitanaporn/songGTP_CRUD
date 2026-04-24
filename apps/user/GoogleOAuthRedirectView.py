from django.views.generic import View
from django.shortcuts import redirect

class GoogleOAuthRedirectView(View):
    """Redirect to allauth's Google login — allauth handles the OAuth flow correctly."""
    def get(self, request):
        next_url = request.GET.get("next")
        if next_url:
            return redirect(f'/accounts/google/login/?next={next_url}')
        else:
            return redirect(f'/accounts/google/login/')