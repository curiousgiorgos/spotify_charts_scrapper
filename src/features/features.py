import spotipy
import sys
import pandas as pd
import numpy as np
from spotipy.oauth2 import SpotifyClientCredentials
from decouple import config

try:
    from .features_model import TrackFeatures, TrackFeaturesList
except ImportError as e:
    from features_model import TrackFeatures, TrackFeaturesList

CLIENT_SECRET = config("CLIENT_SECRET")
CLIENT_ID = config("CLIENT_ID")
INPUT_DATA_PATH = "./data/spotify_charts.csv"
INPUT_DATA_PATH_DEV = "./data/spotify_charts_dev.csv"
OUTPUT_DATA_PATH = "./data/spotify_charts_features.csv"
OUTPUT_DATA_PATH_DEV = "./data/spotify_charts_features_dev.csv"
COLUMNS_TO_DROP = [
    "date",
    "feats",
    "peak_pos",
    "current_pos",
    "prev_pos",
    "streak",
    "streams",
    "country",
    "country_short",
]
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


def spotify_login(cid, secret):
    client_credentials_manager = SpotifyClientCredentials(
        client_id=cid, client_secret=secret
    )
    return spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def features_creation(dev_env):

    sp = spotify_login(CLIENT_ID, CLIENT_SECRET)
    
    file = INPUT_DATA_PATH_DEV if dev_env else INPUT_DATA_PATH 
    df = pd.read_csv(file, encoding="utf-8-sig")
    
    # drop not required columns for performance
    df_songs = df.drop(COLUMNS_TO_DROP, axis=1).drop_duplicates()

    trackFeaturesList = TrackFeaturesList()

    group_size = 50
    grouped = df_songs.groupby(np.arange(len(df_songs)) // group_size)

    # Get the number of groups
    num_groups = grouped.ngroup().nunique()
    for batch_num, batch in grouped:
        print(f"Fetching features for batch {batch_num} out of {num_groups} ")
        batch_uris = batch["track_uri"].tolist()
        artists_uris = batch["artist_uri"].tolist()
        results = sp.audio_features(batch_uris)
        results_art = sp.artists(artists_uris)["artists"]

        artist_genre = {
            track_uri: [artist["genres"][0]] if len(artist["genres"]) > 0 else []
            for track_uri, artist in enumerate(results_art)
        }

        for index, song in enumerate([song for song in results if song]):
            trackFeatures = TrackFeatures(
                batch_uris[index],
                artist_genre[index],
                [song[feature] for feature in FEATURES],
            )
            trackFeaturesList.add_track(trackFeatures)

    df_features = trackFeaturesList.to_dataframe()

    print(f"Features found for {df_features.shape[0]} out of {df_songs.shape[0]} songs")

    # merge the features on the original data, dropping entries that we de
    # didn't find features for
    df_final = pd.merge(df, df_features, on="track_uri", how="inner")

    print(f"Saving dataset, final size: {df_final.shape}")

    if dev_env:
        df_final.to_csv(OUTPUT_DATA_PATH_DEV, index=False, encoding="utf-8-sig")
    else:
        df_final.to_csv(OUTPUT_DATA_PATH, index=False, encoding="utf-8-sig")


def pipeline_features(dev_env=False):
    features_creation(dev_env)


if __name__ == "__main__":
    dev_env = len(sys.argv) > 1 and sys.argv[1] == "dev"
    features_creation(dev_env)
