try:
    from .persistence_model import DimArtist, DimGenre, DimCountry, DimTrack, FactChart
except ImportError as e:
    from persistence_model import DimArtist, DimGenre, DimCountry, DimTrack, FactChart

import pandas as pd
import sys
import sqlalchemy
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect
from decouple import config
from datetime import datetime

DATA_FILE_PATH = "data/spotify_charts_features.csv"
DATA_FILE_DEV_PATH = "data/spotify_charts_features_dev.csv"

DATABASE_LOCATION = config("DATABASE_PATH")
DATABASE_DEV_LOCATION = config("DATABASE_DEV_PATH")


def create_fact_chart(row):
    date_str = row["date"]
    date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

    return FactChart(
        date=date_obj,
        track_uri=row["track_uri"],
        artist_uri=row["artist_uri"],
        genre=row["genre"],
        current_pos=row["current_pos"],
        peak_pos=row["peak_pos"],
        prev_pos=row["prev_pos"],
        streak=row["streak"],
        streams=row["streams"],
        country=row["country"],
        country_short=row["country_short"],
    )


def load(filepath):
    return pd.read_csv(filepath, encoding="utf-8-sig")


def create_dim_artist(row):
    return DimArtist(
        artist=row["artist"], artist_uri=row["artist_uri"], genre=row["genre"]
    )


def create_dim_track(row):
    return DimTrack(
        track=row["track"],
        track_uri=row["track_uri"],
        artist_uri=row["artist_uri"],
        feat=row["feats"],
        energy=row["energy"],
        loudness=row["loudness"],
        mode=row["mode"],
        key=row["key"],
        danceability=row["danceability"],
        speechiness=row["speechiness"],
        acousticness=row["acousticness"],
        instrumentalness=row["instrumentalness"],
        liveness=row["liveness"],
        valence=row["valence"],
        tempo=row["tempo"],
        duration_ms=row["duration_ms"],
        time_signature=row["time_signature"],
    )


def create_dim_country(row):
    return DimCountry(country=row["country"], country_short=row["country_short"])


def create_dim_genre(row):
    return DimGenre(genre=row["genre"])


def persist(dev_env):
    # Future Improvements:
    # 1. Expand logic for dim_artist to pick up differences in artist information
    #    ex. an artist's genre might change
    
    if dev_env:
        charts_df = load(DATA_FILE_DEV_PATH)
        basedir = os.path.abspath(DATABASE_DEV_LOCATION)
    else:
        charts_df = load(DATA_FILE_PATH)
        basedir = os.path.abspath(DATABASE_LOCATION)

    db_engine = sqlalchemy.create_engine(f"sqlite:///{basedir}")

    Session = sessionmaker(bind=db_engine)
    session = Session()

    try:
        # Optimization to duplicate insertions on the database 
        # this leads to a 50% time performance with around 15k datapoints 
        
        tracks = set() 
        countries = set() 
        genres = set()
        artists = set() 
         
        for _, row in charts_df.iterrows():
            if row["track"] not in tracks: 
                dim_track = create_dim_track(row)
                session.merge(dim_track)
                tracks.add(row['track'])
            if row["country"] not in countries: 
                dim_country = create_dim_country(row)
                session.merge(dim_country)                
                countries.add(row['country'])
            if row["genre"] not in genres: 
                dim_genre = create_dim_genre(row)
                session.merge(dim_genre)
                genres.add(row['genre'])
            if row["artist"] not in artists: 
                dim_artist = create_dim_artist(row)
                session.merge(dim_artist)
                artists.add(row["artist"])

            fact_chart = create_fact_chart(row)
            session.merge(fact_chart)
            
        session.commit()
        
    except Exception as e:
        print(f"Error: {e}")
        session.rollback()
    finally:
        print("Data persisted")
        session.close()


def pipeline_persistence(dev_env=False):
    persist(dev_env)


if __name__ == "__main__":
    dev_env = len(sys.argv) > 1 and sys.argv[1] == "dev"
    persist(dev_env)
