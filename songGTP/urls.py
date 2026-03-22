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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# Import all view functions
from user.views import get_user, create_user, update_user, delete_user, create_user_template
from song.views import get_song, create_song, update_song, delete_song
from prompt.views import get_prompt, create_prompt, update_prompt, delete_prompt
from library.views import get_library, create_library, update_library, delete_library

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # USER ENDPOINTS
    path('api/users/', get_user, name='get_user'),
    path('api/users/create/', create_user, name='create_user'),
    path('api/users/update/<int:pk>/', update_user, name='update_user'),
    path('api/users/delete/<int:pk>/', delete_user, name='delete_user'),
    
    # SONG ENDPOINTS
    path('api/songs/', get_song, name='get_song'),
    path('api/songs/create/', create_song, name='create_song'),
    path('api/songs/update/<int:pk>/', update_song, name='update_song'),
    path('api/songs/delete/<int:pk>/', delete_song, name='delete_song'),
    
    # PROMPT ENDPOINTS
    path('api/prompts/', get_prompt, name='get_prompt'),
    path('api/prompts/create/', create_prompt, name='create_prompt'),
    path('api/prompts/update/<int:pk>/', update_prompt, name='update_prompt'),
    path('api/prompts/delete/<int:pk>/', delete_prompt, name='delete_prompt'),
    
    # LIBRARY ENDPOINTS
    path('api/libraries/', get_library, name='get_library'),
    path('api/libraries/create/', create_library, name='create_library'),
    path('api/libraries/update/<int:pk>/', update_library, name='update_library'),
    path('api/libraries/delete/<int:pk>/', delete_library, name='delete_library'),
    
    path('create-user/', create_user_template, name="create_user_template")
]
