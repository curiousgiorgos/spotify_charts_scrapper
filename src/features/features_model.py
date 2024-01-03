import pandas as pd

FEATURES = [
    "danceability",
    "energy",
    "key",
    "loudness",
    "mode",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "tempo",
    "duration_ms",
    "time_signature",
]


class TrackFeatures:
    def __init__(self, track_uri=None, genre=None, features=None):
        self.track_uri = track_uri
        self.genre = genre
        self.features = {
            FEATURES[index]: feature for index, feature in enumerate(features)
        }

    def to_dict(self):
        return {
            "track_uri": self.track_uri,
            "genre": self.genre,
            "features": self.features,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def __str__(self):
        dic_form = self.to_dict()
        return ", ".join([f"{key}: {value}" for key, value in dic_form.items()])


class TrackFeaturesList:
    def __init__(self, tracks=None):
        self.tracks = tracks or []

    def add_track(self, track):
        self.tracks.append(track)

    def to_dataframe(self):
        # Create a list of dictionaries representing each entry
        entries = [
            {
                "track_uri": track.track_uri,
                "genre": track.genre,
                **{feature: track.features[feature] for feature in FEATURES},
            }
            for track in self.tracks
        ]

        # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame(entries)

        return df
