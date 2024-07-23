from django.urls import path
from .views import (
    RegistrationView,
    LoginView,
    ProfileView,
    PlaylistView,
)

urlspatterns = [
    # Authentication
    path("register/", RegistrationView.as_view()),
    path("login/", LoginView.as_view()),
    # Profile
    path("profile/", ProfileView.as_view()),
    # Playlist
    path("playlist/", PlaylistView.as_view()),
]
