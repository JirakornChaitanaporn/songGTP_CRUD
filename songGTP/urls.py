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
from apps.user.views import UserViewController, CreateUserView, SearchUserView , DeleteUserView , UseLoginView, LogoutView
from apps.song.views import SongViewController, CreateSongView, SearchSongView, DeleteSongView, UpdateSongView , SongView
from apps.prompt.views import PromptViewController, CreatePromptView, SearchPromptView, DeletePromptView, UpdatePromptView, GenerateSongView , SunoStatusViewController , CreatePromptMockupView
from apps.library.views import LibraryViewController, CreateLibraryView, SearchLibraryView, DeleteLibraryView, UpdateLibraryView, LibraryView
from apps.home.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    
    path('', HomeView.as_view(), name="home"),
    path('sign-in/', UseLoginView.as_view(), name="sign_in"),
    path('sign-up/', CreateUserView.as_view(), name="sign_up"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('library/', LibraryView.as_view(), name="library"),
    path('song/', SongView.as_view(), name="song"),
    path('generate_song/<int:lid>', GenerateSongView.as_view(), name="generate_song"),
    
    # USER ENDPOINTS
    path('api/users/', UserViewController.as_view()),
    path('api/users/<int:pk>', UserViewController.as_view()),
    
    # SONG ENDPOINTS
    path('api/songs/', SongViewController.as_view()),
    path('api/songs/<int:pk>', SongViewController.as_view()),
    
    # PROMPT ENDPOINTS
    path('api/prompts/', PromptViewController.as_view()),
    path('api/prompts/<int:pk>', PromptViewController.as_view()),
    path('api/suno-status/<str:tid>/<int:lid>', SunoStatusViewController.as_view()),
    
    # LIBRARY ENDPOINTS
    path('api/libraries/', LibraryViewController.as_view()),
    path('api/libraries/<int:pk>', LibraryViewController.as_view()),
    
    
    # Alternative CRUD (Template Views)
    # User
    path('create-user/', CreateUserView.as_view(), name="sign_up_template"),
    path('search-user/', SearchUserView.as_view(), name="search_user"),
    path('delete-user/', DeleteUserView.as_view(), name="delete_user_template"),
    # path('update-user/', UpdateUserView.as_view(), name = "update_user_template"),
    # Song
    path('create-song/', CreateSongView.as_view(), name="create_song_template"),
    path('search-song/', SearchSongView.as_view(), name="search_song"),
    path('delete-song/', DeleteSongView.as_view(), name="delete_song_template"),
    path('update-song/', UpdateSongView.as_view(), name="update_song_template"),
    # Library
    path('create-library/', CreateLibraryView.as_view(), name="create_library_template"),
    path('search-library/', SearchLibraryView.as_view(), name="search_library"),
    path('delete-library/', DeleteLibraryView.as_view(), name="delete_library_template"),
    path('update-library/', UpdateLibraryView.as_view(), name="update_library_template"),
    # Prompt
    path('create-prompt/', CreatePromptView.as_view(), name="create_prompt_template"),
    path('search-prompt/', SearchPromptView.as_view(), name="search_prompt"),
    path('delete-prompt/', DeletePromptView.as_view(), name="delete_prompt_template"),
    path('update-prompt/', UpdatePromptView.as_view(), name="update_prompt_template"),
    path('create-prompt-mockup/<int:lid>', CreatePromptMockupView.as_view(), name="create_prompt_mockup"),

]

