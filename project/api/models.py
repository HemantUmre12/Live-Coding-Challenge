class Playlist:
    def __init__(self, name, description, songs=None):
        self.name = name
        self.description = description
        self.songs = songs if songs is not None else []


class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.name = ""
        # URL or path to image
        self.profile_picture = None
        self.bio = ""
        self.playlists = {}

    def check_password(self, enteredPassword):
        return enteredPassword == self.password

    def update_profile(self, name, profile_picture, bio):
        if name:
            self.name = name

        if profile_picture:
            self.profile_picture = profile_picture

        if bio:
            self.bio = bio