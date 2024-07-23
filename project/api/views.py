from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Playlist

# In-memory storage for users
users_db = {}


class RegistrationView(APIView):
    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        if username in users_db:
            return Response(
                {"message": "User already exists"}, status=status.HTTP_400_BAD_REQUEST
            )

        user = User(username, email, password)
        users_db[username] = user
        return Response(
            {"message": "User registered successfully"}, status=status.HTTP_201_CREATED
        )


class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = users_db.get(username)

        if not user or not user.check_password(password):
            return Response(
                {"message": "Invalid username or password"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response({"message": "Login successful"}, status=status.HTTP_200_OK)


class ProfileView(APIView):
    def post(self, request):
        username = request.data.get("username")
        user = users_db.get(username)
        if not user:
            return Response(
                {"message": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        name = request.data.get("name")
        profile_picture = request.data.get("profile_picture")
        bio = request.data.get("bio")

        user.update_profile(name, profile_picture, bio)
        return Response(
            {"message": "Profile updated successfully"}, status=status.HTTP_200_OK
        )

    def get(self, request):
        username = request.data.get("username")
        user = users_db.get(username)
        if not user:
            return Response(
                {"message": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        profile_data = {
            "username": user.username,
            "email": user.email,
            "name": user.name,
            "profile_picture": user.profile_picture,  # This should be a URL or a path to the image
            "bio": user.bio,
        }

        return Response(profile_data, status.HTTP_200_OK)


class PlaylistView(APIView):
    def post(self, request):
        username = request.data.get("username")
        user = users_db.get(username)
        if not user:
            return Response(
                {"message": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        playlist_name = request.data.get("name")
        description = request.data.get("description")

        if playlist_name in user.playlists:
            return Response(
                {"message": "Playlist already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        playlist = Playlist(name=playlist_name, description=description)
        user.playlists[playlist_name] = playlist
        return Response(
            {"message": "Playlist created successfully"}, status=status.HTTP_201_CREATED
        )

    def put(self, request):
        username = request.data.get("username")
        user = users_db.get(username)
        if not user:
            return Response(
                {"message": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        playlist_name = request.data.get("name")
        new_name = request.data.get("new_name")
        new_description = request.data.get("new_description")
        new_songs = request.data.get("new_songs", [])

        if playlist_name not in user.playlists:
            return Response(
                {"message": "Playlist not found"}, status=status.HTTP_404_NOT_FOUND
            )

        playlist = user.playlists[playlist_name]
        if new_name:
            user.playlists[new_name] = user.playlists.pop(playlist_name)
            playlist.name = new_name
        if new_description:
            playlist.description = new_description
        if new_songs:
            playlist.songs = new_songs

        return Response(
            {"message": "Playlist updated successfully"}, status=status.HTTP_200_OK
        )

    def delete(self, request):
        username = request.data.get("username")
        user = users_db.get(username)
        if not user:
            return Response(
                {"message": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        playlist_name = request.data.get("name")

        if playlist_name not in user.playlists:
            return Response(
                {"message": "Playlist not found"}, status=status.HTTP_404_NOT_FOUND
            )

        del user.playlists[playlist_name]
        return Response(
            {"message": "Playlist deleted successfully"}, status=status.HTTP_200_OK
        )

    def get(self, request):
        username = request.data.get("username")
        user = users_db.get(username)
        if not user:
            return Response(
                {"message": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        playlist_name = request.data.get("name")
        playlist = user.playlists.get(playlist_name)
        if not playlist:
            return Response(
                {"message": "Playlist not found"}, status=status.HTTP_404_NOT_FOUND
            )

        playlist_data = {
            "name": playlist.name,
            "description": playlist.description,
            "songs": playlist.songs,
        }
        return Response(playlist_data, status=status.HTTP_200_OK)
