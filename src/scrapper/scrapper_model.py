import pandas as pd

class SpotifyChartEntry:
    def __init__(
        self,
        date,
        track,
        artist,
        feats,
        current_pos,
        peak_pos,
        prev_pos,
        streak,
        streams,
        country,
        country_short,
        track_uri,
        artist_uri,
    ):
        self.date = date
        self.track = track
        self.artist = artist
        self.feats = feats
        self.current_pos = current_pos
        self.peak_pos = peak_pos
        self.prev_pos = prev_pos
        self.streak = streak
        self.streams = streams
        self.country = country
        self.country_short = country_short
        self.track_uri = track_uri
        self.artist_uri = artist_uri

    def to_dict(self):
        return {
            "date": self.date,
            "track": self.track,
            "artist": self.artist,
            "feats": self.feats,
            "current_pos": self.current_pos,
            "peak_pos": self.peak_pos,
            "prev_pos": self.prev_pos,
            "streak": self.streak,
            "streams": self.streams,
            "country": self.country,
            "country_short": self.country_short,
            "track_uri": self.track_uri,
            "artist_uri": self.artist_uri,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def __str__(self):
        dic_form = self.to_dict()
        return ", ".join([f"{key}: {value}" for key, value in dic_form.items()])


class SpotifyCountryList:
    def __init__(self, name, short_name, entries=None):
        self.name = name
        self.short_name = short_name
        self.entries = entries or []

    COLUMN_NAMES = [
        "date", "track", "artist", "feats", "current_pos", "peak_pos", "prev_pos",
        "streak", "streams", "country", "country_short", "track_uri", "artist_uri"
    ]
    
    def add_entry(self, entry):
        self.entries.append(entry)

    def to_dataframe(self):
        # Create a list of dictionaries representing each entry
        entries = [entry.to_dict() for entry in self.entries]

        # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame(
            entries,
            columns=self.COLUMN_NAMES,
        )

        return df

    def to_dict(self):
        return {
            "name": self.name,
            "short_name": self.short_name,
            "entries": [entry.to_dict() for entry in self.entries],
        }

    @classmethod
    def from_dict(cls, data):
        name = data["name"]
        short_name = data["short_name"]
        entries_data = data["entries"]
        entries = [
            SpotifyChartEntry.from_dict(entry_data) for entry_data in entries_data
        ]
        return cls(name, short_name, entries)

    def __str__(self):
        return f"Country: {self.name}, Short Name: {self.short_name}, Entries: {len(self.entries)}"
