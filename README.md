# spotify_scrapper

## An Apache Airflow Spotify charts scrapper

An Apache Airflow pipeline that runs on a weekly basis to scrape the Top 200 tracks per country on Spotify.
The tracks are scrapped from **spotifycharts.com** and the features of the songs are extracted from the **Spotify API**

You can also use the standalone scripts directly if you want to only scrape the data and not use the pipeline. Refer to the **Manual run** section for more information.

Feel free to use/ extend this script. Just make sure to reference me and this repository!

## Scripts deep-dive

All the relevat scripts can be found under **/src**

1. spotify_dag.py
   1. Defines a simple dag to run on a weekly basis to extract the data
   2. The steps defined in the bag utilize the scripts described below
2. scrapper.py
   1. Scrappes **spotifycharts.com**. Iterarates through the country list defines under **countries_lists/countries.txt** and extracts the data
   2. Creates a csv file of the data under the **/data** directory
3. features.py
   1. Uses the **Spotify API** to fetch the features of the songs that were scrapped in step 2.
   2. Outputs a csv including the songs with their features attached
4. create_database.py
   1. Creates an sqlite database according to the scripts defined in **sql/create-owner-objects-1.0.0.0.sql**
   2. A dev database is created to use for dev purposes
5. persistence.py
   1. Persists the data on the database creates in step 4 using sqlachemy
6. main.py
   1. Python script to run the pipeline steps directly
   2. This can be utilized if you do not want to settup/ use airflow and run the pipeline manually
   3. **dev** can be based as an argument to run the scripts with a subset of the target countries

## Dev environmnet

A development mode is also supported. The dev moded uses only a subset of the target countries. The countries to be used can be set in `lists/countries_short.txt`.
To manually run in development mode use:

`python src/main.py dev` from the main directory

The script data and database will have the `_dev` suffix

## Database schema

fact_carts
| Column | Key | Nullable | Type |
| ---- | ---- | ---- |
| track_uri | PK, FK to tracks | No | VARCHAR
| artist_uri | FK to artists| No | VARCHAR
| genres | | No | VARCHAR
| date | PK | No | DATE
| current_pos | | No | SMALLINT
| peak_pos | | Yes | SMALLINT
| prev_pos | | Yes | SMALLINT
| streak | | Yes | SMALLINT
| streams | | Yes | INT
| country | | No | VARCHAR
| country_short | PK, FK to countries | No | VARCHAR

dim_tracks
| Column | Key | Nullable | Type |
| ---- | ---- | ---- | ---- |
| track | FK to genres| No | VARCHAR
| track_uri | PK | No | VARCHAR
| artist_uri | | No | VARCHAR
| feat | | Yes | VARCHAR
| energy | | Yes | DECIMAL(8, 2)
| loudness | | Yes | DECIMAL(8, 2)
| mode | | Yes | DECIMAL(8, 2)
| key | | Yes| DECIMAL(8, 2)
| danceability | | Yes | DECIMAL(8, 2)
| spechiness | | Yes | DECIMAL(8, 2)
| acousticness | | Yes | DECIMAL(8, 2)
| instrumentalness | | Yes | DECIMAL(8, 2)
| liveness | | Yes | DECIMAL(8, 2)
| valence | | Yes | DECIMAL(8, 2)
| tempo | | Yes | INT
| duration_ms || Yes | INT
| time_signature | | Yes | INT

dim_artists
| Column | Key | Nullable | Type |
| ---- | ---- | ---- | ---- |
| country | | No | VARCHAR
| country_short | PK | No | VARCHAR

dim_genres
| Column | Key | Nullable | Type |
| ---- | ---- | ---- | ---- |
| genre | PK | No | VARCHAR

dim_countries
| Column | Key | Nullable | Type |
| ---- | ---- | ---- | ---- |
| artist | | No | VARCHAR
| artist_uri | PK | No | VARCHAR
| genre | | No | VARCHAR

## Required modules

1. BeautifulSoup
2. Selenium
3. Airflow
4. Pandas

## .env

Throughout the application configurations are pulled from `.env`. This includes sensitive information and you would thus have to create and populate the file on your own.

The required information are

- `SPOTIFY_USERNAME` : username to log in to spotifycharts
- `SPOTIFY_PASSWORD` : password to log in to spotifycharts
- `CLIENT_ID` : your applications' ID
- `CLIENT_SECRET`: your applications' secret
- `DATABASE_PATH` : path to your database location
- `DATABASE_DEV_PATH` : path to your development database

Example:
`SPOTIFY_USERNAME=curiousgiorgos`

## Manual run

If you do not want to use the pipeline, inside src there exists a `main.py` file to manually run the steps of the pipeline.
Doing so will:

- Scrape the website
- Retrieve the features from the **Spotify API**
- Create the main and dev databases in SQLITE
- Persist the data into the databaases

Additionally, if you want to only scrape `spotifycharts` you can directly run it with `python scrappe.py` to just scrape the site.
Note: ensure that you have set up the requirement in `.env`

## Future improvements

1. Currently the script scrapes the data only for the current day. A natural future improvement would be to extend the script to scrape old/ target dates. This can be done easily through the usage of the `url_crafter.py` script that creates the urls to scrape the data from.

2. Currently I have implemented an optimization in order to avoid duplicate insertions in the dimension tables. This leades to a 50% time improvement for a given dataset (ex. 15k entries 20 sec vs 44 sec). This can further be extended to first fetch the current entries in the database and then only insert the new ones to the db. Although I believe that the performance improvement will be minimal due to to the small number of entries

## FAQ

#### How do I bypass the captcha?

The first time the script runs you might be required to pass a captcha. In order to do so you can manually log in to `spotifychats.com` on your broswer or commenet out the `headless` configuration in the script and log in from the selenium window.

In following runs the issue will not arise

#### There was a failure in the scrapper, what to do?

In rare cases the scrapper can fail, either in the log in portion or when navigating between pages.

Simply running the script again (or through re-tries in the airflow pipeline) should resolve the issue

A future extension in the above could be to include fault-tolerance and automatic retries in case of failures

This repository also includes the database with the weekly data for week 09/13/2022-09/19/2022 as well as a PBI file showcasing the data.
