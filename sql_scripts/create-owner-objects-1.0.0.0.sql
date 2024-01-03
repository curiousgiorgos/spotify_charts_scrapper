CREATE TABLE IF NOT EXISTS dim_genres (
    genre VARCHAR,
    PRIMARY KEY (genre)
);

CREATE TABLE IF NOT EXISTS dim_artists (
    artist VARCHAR,
    artist_uri VARCHAR,
    genre VARCHAR, 
    PRIMARY KEY (artist_uri),
    FOREIGN KEY (genre) REFERENCES dim_genres(genre)
);

CREATE TABLE IF NOT EXISTS dim_countries (
    country VARCHAR,
    country_short VARCHAR,
    PRIMARY KEY (country_short)
);

CREATE TABLE IF NOT EXISTS dim_tracks (
    track VARCHAR,
    track_uri VARCHAR,
    artist_uri VARCHAR,
    feat VARCHAR,
    energy DECIMAL(8, 2),
    loudness DECIMAL(8, 2),
    mode DECIMAL(8, 2),
    key DECIMAL(8, 2),
    danceability DECIMAL(8, 2),
    speechiness DECIMAL(8, 2),
    acousticness DECIMAL(8, 2),
    instrumentalness DECIMAL(8, 2),
    liveness DECIMAL(8, 2),
    valence DECIMAL(8, 2),
    tempo INT,
    duration_ms INT,
    time_signature INT,
    PRIMARY KEY (track_uri)
);

CREATE TABLE IF NOT EXISTS fact_charts (
    date DATE,
    track_uri VARCHAR,
    artist_uri VARCHAR,
    genre VARCHAR,
    current_pos SMALLINT,
    peak_pos SMALLINT,
    prev_pos SMALLINT,
    streak SMALLINT,
    streams INT,
    country VARCHAR,
    country_short VARCHAR,
    PRIMARY KEY (date, country_short, track_uri),
    FOREIGN KEY (artist_uri) REFERENCES dim_artists(artist_uri),
    FOREIGN KEY (track_uri) REFERENCES dim_tracks(track_uri),
    FOREIGN KEY (country_short) REFERENCES dim_countries(country_short)
);