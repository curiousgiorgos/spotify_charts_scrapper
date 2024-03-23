# Spotify Scraper with Apache Airflow

## Overview

This project comprises an Apache Airflow pipeline designed to run weekly, scraping the Top 200 tracks per country from **spotifycharts.com**. The scraped data is complemented with song features extracted from the **Spotify API**.

Feel free to utilize or extend this script with proper attribution to the original repository.

## Index

- [Spotify scraper with Apache Airflow](#spotify-scraper-with-apache-airflow)
  - [Overview](#overview)
  - [Index](#index)
  - [Scripts Overview](#scripts-overview)
  - [Development Environment](#development-environment)
  - [Database Schema](#database-schema)
    - [`fact_charts`](#fact_charts)
    - [`dim_tracks`](#dim_tracks)
    - [`dim_artists`](#dim_artists)
    - [`dim_genres`](#dim_genres)
    - [`dim_countries`](#dim_countries)
  - [Power BI File](#power-bi-file)
  - [Requirements](#requirements)
    - [Modules](#modules)
    - [.env Configuration](#env-configuration)
  - [Manual Execution](#manual-execution)
  - [Future Improvements](#future-improvements)
  - [FAQ](#faq)
    - [How to Bypass the Captcha?](#how-to-bypass-the-captcha)
    - [Handling Scraper Failures](#handling-scraper-failures)
  - [Using/ incorporating this repository](#using-incorporating-this-repository)

## Scripts Overview

All relevant scripts are located under **/src**.

1. **spotify_dag.py**

   - Defines an Apache Airflow DAG to run on a weekly basis, orchestrating the data extraction steps.

2. **scraper.py**

   - Scrapes **spotifycharts.com** by iterating through a list of countries defined in **countries_lists/countries.txt**.
   - Creates a CSV file containing the scraped data in the **/data** directory.

3. **features.py**

   - Utilizes the **Spotify API** to fetch features of the songs scraped in the previous step.
   - Outputs a CSV file containing songs with attached features.

4. **create_database.py**

   - Creates an SQLite database according to the scripts defined in **sql/create-owner-objects-1.0.0.0.sql**.
   - Establishes a separate dev database for development purposes.

5. **persistence.py**

   - Persists the data in the database created in the previous step using SQLAlchemy.

6. **main.py**
   - Python script to manually run the pipeline steps without setting up Apache Airflow.
   - Supports a **dev** mode with a subset of target countries.

## Development Environment

A development mode is supported, utilizing a subset of target countries. The countries to be used can be set in `lists/countries_short.txt`. To manually run in development mode, use:

```bash
python src/main.py dev
```

The script and database for development will have the \_dev suffix.

## Database Schema

### `fact_charts`

| Column        | Key | Nullable | Type     |
| ------------- | --- | -------- | -------- |
| track_uri     | PK  | No       | VARCHAR  |
| artist_uri    | FK  | No       | VARCHAR  |
| genres        |     | No       | VARCHAR  |
| date          | PK  | No       | DATE     |
| current_pos   |     | No       | SMALLINT |
| peak_pos      |     | Yes      | SMALLINT |
| prev_pos      |     | Yes      | SMALLINT |
| streak        |     | Yes      | SMALLINT |
| streams       |     | Yes      | INT      |
| country       |     | No       | VARCHAR  |
| country_short | PK  | No       | VARCHAR  |

### `dim_tracks`

| Column           | Key | Nullable | Type          |
| ---------------- | --- | -------- | ------------- |
| track            | FK  | No       | VARCHAR       |
| track_uri        | PK  | No       | VARCHAR       |
| artist_uri       |     | No       | VARCHAR       |
| feat             |     | Yes      | VARCHAR       |
| energy           |     | Yes      | DECIMAL(8, 2) |
| loudness         |     | Yes      | DECIMAL(8, 2) |
| mode             |     | Yes      | DECIMAL(8, 2) |
| key              |     | Yes      | DECIMAL(8, 2) |
| danceability     |     | Yes      | DECIMAL(8, 2) |
| spechiness       |     | Yes      | DECIMAL(8, 2) |
| acousticness     |     | Yes      | DECIMAL(8, 2) |
| instrumentalness |     | Yes      | DECIMAL(8, 2) |
| liveness         |     | Yes      | DECIMAL(8, 2) |
| valence          |     | Yes      | DECIMAL(8, 2) |
| tempo            |     | Yes      | INT           |
| duration_ms      |     | Yes      | INT           |
| time_signature   |     | Yes      | INT           |

### `dim_artists`

| Column        | Key | Nullable | Type    |
| ------------- | --- | -------- | ------- |
| country       |     | No       | VARCHAR |
| country_short | PK  | No       | VARCHAR |

### `dim_genres`

| Column | Key | Nullable | Type    |
| ------ | --- | -------- | ------- |
| genre  | PK  | No       | VARCHAR |

### `dim_countries`

| Column     | Key | Nullable | Type    |
| ---------- | --- | -------- | ------- |
| artist     |     | No       | VARCHAR |
| artist_uri | PK  | No       | VARCHAR |
| genre      |     | No       | VARCHAR |

## Power BI File

This repository also includes a Power BI (PBI) file providing a visual representation and analysis of the weekly data. The PBI file can be found in the repository, and it serves as a convenient tool for exploring and gaining insights from the Spotify charts data.

To make use of the Power BI file:

1. Open the file in Power BI Desktop.
2. Connect the file to the appropriate database or data source.
3. Explore the pre-built visualizations and dashboards to analyze the Spotify charts data.

You might require to setup ODBC for sqlite in order to re-connect the database.

## Requirements

### Modules

1. BeautifulSoup
2. Selenium
3. Apache Airflow
4. Pandas

### .env Configuration

Sensitive information is stored in the .env file, including:

- SPOTIFY_USERNAME: Spotify.com username
- SPOTIFY_PASSWORD: Spotify.com password
- CLIENT_ID: Spotify API Application ID
- CLIENT_SECRET: Spotify API Application secret
- DATABASE_PATH: Path to the main database
- DATABASE_DEV_PATH: Path to the development database

Example:

```env
SPOTIFY_USERNAME=your_username
SPOTIFY_PASSWORD=your_password
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
DATABASE_PATH=/path/to/main/database
DATABASE_DEV_PATH=/path/to/dev/database
```

## Manual Execution

If you prefer not to use the AThe PBI file is designed to enhance the user experience by offering a dynamic and interactive way to interpret the weekly music charts.

Feel free to customize the Power BI file based on your specific requirements and preferences.
in the src directory to manually run the pipeline steps. This will:

1. Scrape the website
2. Retrieve features from the Spotify API
3. Create main and dev databases in SQLite
4. Persist the data into the databases

Additionally, if you only want to scrape spotifycharts,

```bash
python src/scraper.py
```

Ensure that you have set up the requirements in .env.

## Future Improvements

1. Date Range Scraping

   - Currently, the script scrapes data only for the current day. Consider extending it to scrape old/target dates using the url_crafter.py script for creating URLs.

2. Optimizations for Duplicate Insertions
   - Extend the optimization to fetch current entries in the database and insert only new ones, reducing redundant operations.

## FAQ

### How to Bypass the Captcha?

The first time the script runs, you might need to pass a captcha. Manually log in to spotifycharts.com on your browser or comment out the headless configuration in the script to log in from the Selenium window.

In subsequent runs, the issue will not arise.

### Handling Scraper Failures

In rare cases, the scraper might fail during login or page navigation. Simply running the script again (or through retries in the Apache Airflow pipeline) should resolve the issue.

## Using/ incorporating this repository

Feel free to adjust the content based on your preferences and project specifics but please make sure to reference and give credit to this repository.
