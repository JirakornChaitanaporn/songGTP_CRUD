"""
URL configuration for songGTP project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Import all view functions
# from apps.user.views import UserLoginView, LogoutView, GoogleOAuthRedirectView
# from apps.song.views import SongView, DownloadSongView, PublicSongView, PatchSharingStatusView
# from apps.prompt.views import GenerateSongView , CreatePromptMockupView, ShowPrompt
# from apps.library.views import LibraryView
# from apps.home.views import HomeView
from apps.user.GoogleOAuthRedirectView import  GoogleOAuthRedirectView
from apps.user.LogoutView import LogoutView
from apps.user.UserLoginView import UserLoginView
from apps.song.GetDownloadSongView import GetDownloadSongView
from apps.song.GetPublicSongView import GetPublicSongView
from apps.song.GetSongView import GetSongView
from apps.song.DeleteSongView import DeleteSongView
from apps.song.PatchSharingStatusView import PatchSharingStatusView
from apps.prompt.CreateGenerateSongView import CreateGenerateSongView
from apps.prompt.CreatePromptMockupView import CreatePromptMockupView
from apps.prompt.ShowPrompt import ShowPrompt
from apps.library.GetLibraryView import GetLibraryView
from apps.home.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    #google auth
    path('accounts/', include('allauth.urls')),
    
    path('login/', UserLoginView.as_view(), name="login"),
    
    path('auth/google/', GoogleOAuthRedirectView.as_view(), name="google_auth"),
    
    path('logout/', LogoutView.as_view(), name="logout"),
    
    path('', HomeView.as_view(), name="home"),
    
    path('library/', GetLibraryView.as_view(), name="library"),
    
    path('song/', GetSongView.as_view(), name="song"),
    
    path('song/<int:pk>', GetSongView.as_view(), name="song"),
    
    path('shared_song/', GetPublicSongView.as_view(), name="shared_song"),
    
    path('song/<int:pk>/download', GetDownloadSongView.as_view(), name="download_song"),
    
    path('song/<int:pk>/share-toggle/', PatchSharingStatusView.as_view(), name="patch_sharing_status"),
    
    path('generate_song/', CreateGenerateSongView.as_view(), name="generate_song"),
    
    path('show_prompt/', ShowPrompt.as_view(), name="show_prompt"), #add user id to the back later
    
    path('create-prompt-mockup/', CreatePromptMockupView.as_view(), name="create_prompt_mockup"),

    path('delete-song', DeleteSongView.as_view(), name="delete_song_template")
]

