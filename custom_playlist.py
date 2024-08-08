class CustomPlaylist:
    def __init__(self):
        self.tracks = []

    def add_track(self, name, artist):
        self.tracks.append({'name': name, 'artist': artist})

    def get_track(self, index):
        return self.tracks[index]

    def get_total_tracks(self):
        return len(self.tracks)
