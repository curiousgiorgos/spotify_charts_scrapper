from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import PrimaryKeyConstraint

Base = declarative_base()


class FactChart(Base):
    __tablename__ = "fact_charts"

    date = Column(Date, primary_key=True)
    track_uri = Column(String, ForeignKey("dim_tracks.track_uri"), primary_key=True)
    country_short = Column(
        String,
        ForeignKey("dim_countries.country_short"),
        primary_key=True,
        nullable=False,
    )
    artist_uri = Column(String, ForeignKey("dim_artists.artist_uri"), nullable=False)
    genre = Column(String)
    current_pos = Column(Integer)
    peak_pos = Column(Integer)
    prev_pos = Column(Integer)
    streak = Column(Integer)
    streams = Column(Integer)
    country = Column(String, nullable=False)

    # Relationships
    chartsArtists = relationship("DimArtist", back_populates="artistsCharts")
    chartsCountries = relationship("DimCountry", back_populates="countriesCharts")
    chartsTracks = relationship("DimTrack", back_populates="tracksCharts")

    # Define the composite primary key
    __table_args__ = (PrimaryKeyConstraint("date", "track_uri", "country_short"),)


class DimArtist(Base):
    __tablename__ = "dim_artists"

    artist = Column(String, primary_key=True)
    artist_uri = Column(String, primary_key=True)
    genre = Column(String, ForeignKey("dim_genres.genre"), nullable=False)

    # Relationships
    artistsCharts = relationship("FactChart", back_populates="chartsArtists")
    artistsGenres = relationship("DimGenre", back_populates="genresArtists")
  
    

class DimTrack(Base):
    __tablename__ = "dim_tracks"

    track = Column(String)
    track_uri = Column(String, primary_key=True)
    artist_uri = Column(String, nullable=False)
    feat = Column(String)
    energy = Column(Float(precision=5, asdecimal=True))
    loudness = Column(Float(precision=5, asdecimal=True))
    mode = Column(Float(precision=5, asdecimal=True))
    key = Column(Float(precision=5, asdecimal=True))
    danceability = Column(Float(precision=5, asdecimal=True))
    speechiness = Column(Float(precision=5, asdecimal=True))
    acousticness = Column(Float(precision=5, asdecimal=True))
    instrumentalness = Column(Float(precision=5, asdecimal=True))
    liveness = Column(Float(precision=5, asdecimal=True))
    valence = Column(Float(precision=5, asdecimal=True))
    tempo = Column(Integer)
    duration_ms = Column(Integer)
    time_signature = Column(Integer)

    # Relationships
    tracksCharts = relationship("FactChart", back_populates="chartsTracks")

class DimCountry(Base):
    __tablename__ = "dim_countries"

    country = Column(String)
    country_short = Column(String, primary_key=True)

    # Relationships
    countriesCharts = relationship("FactChart", back_populates="chartsCountries")


class DimGenre(Base):
    __tablename__ = "dim_genres"

    genre = Column(String, primary_key=True)

    # Relationships
    genresArtists = relationship("DimArtist", back_populates="artistsGenres")
