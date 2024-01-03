import pandas as pd
import sys

from decouple import config
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from time import sleep

try: 
    from .scrapper_model import SpotifyChartEntry, SpotifyCountryList
    from .utils.url_crafter import create_urls
    from .utils.date_resolver import get_closest_past_thursday
except ImportError as e:
    from scrapper_model import SpotifyChartEntry, SpotifyCountryList
    from utils.url_crafter import create_urls
    from utils.date_resolver import get_closest_past_thursday


URL = "https://accounts.spotify.com/en/login?continue=https%3A%2F%2Fcharts.spotify.com/login"
USERNAME = config("SPOTIFY_USERNAME")
PASSWORD = config("SPOTIFY_PASSWORD")
OUTPUT_PATH = "./data/spotify_charts.csv"
OUTPUT_PATH_DEV = "./data/spotify_charts_dev.csv"

def init_driver(dev_env=False):
    firefox_options = Options()
    firefox_options.set_preference("browser.download.folderList", 2)
    firefox_options.set_preference("browser.download.manager.showWhenStarting", False)
    firefox_options.set_preference(
        "browser.helperApps.neverAsk.saveToDisk", "application/x-gzip"
    )
    if not dev_env:
        firefox_options.add_argument("--headless")
    driver = Firefox(options=firefox_options)
    wait = WebDriverWait(driver, 5)
    return driver, wait


def login(max_attempts, driver, wait):
    for attempt in range(max_attempts):
        driver.get(URL)
        driver.find_element(By.ID, "login-username").send_keys(USERNAME)
        driver.find_element(By.ID, "login-password").send_keys(PASSWORD)
        sleep(0.5)
        driver.find_element(By.ID, "login-button").click()

        try:
            # doesnt work, need to check the other case too
            wait.until(EC.presence_of_element_located((By.ID, "#login=button")))
            # if the element is found, login is unsuccessful
            print(f"Login attempt {attempt + 1} failed. Retrying...")
            sleep(2)
        except TimeoutException:
            print("Login successful.")
            break
    else:
        print("Max login attempts reached. Login unsuccessful. Exiting")
        exit(1)


def extract_data(country, country_short, url, driver, wait):

    print(f"Scrapping {country}")
    driver.get(url)
    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, f"//a[contains(@href, '/charts/overview/{country_short}')]")
        )
    )
    
    date = get_closest_past_thursday()
    spotifyCountryList = SpotifyCountryList(country, country_short)

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "lxml")

    for pos, tr in enumerate(soup.find("table").findAll("tr")[1:]):
        entry = [i for i in tr.findAll("a")][1:]

        track = entry[0].text[1:]
        artist = entry[1].text
        feats = []
        for i in entry[2:]:
            feats.append(i.text)
        current_pos = pos + 1
        track_uri = entry[0]["href"].split("/")[-1]
        artist_uri = entry[1]["href"].split("/")[-1]
        stream_info = [i.text for i in tr.findAll("td")]
        peak_pos = int(stream_info[-6])
        prev_pos = int(stream_info[-5]) if stream_info[-5].isnumeric() else "NaN"
        streak = int(stream_info[-4]) if stream_info[-4].isnumeric() else "NaN"
        streams = int(stream_info[-3].replace(",", ""))

        spotifyChartEntry = SpotifyChartEntry(
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
        )
        spotifyCountryList.add_entry(spotifyChartEntry)

    return spotifyCountryList.to_dataframe()


def scrape(driver, wait, dev_env=False):
    login(5, driver, wait)

    # fetch urls, subset of urls if in development mode
    country_links = create_urls(dev_env)
    country_dfs = []
    for country, country_short, url in country_links:
        country_df = extract_data(country, country_short, url, driver, wait)
        country_dfs.append(country_df)
    
    all_countries_df = pd.concat(country_dfs, ignore_index=True)
    all_countries_df.to_csv(OUTPUT_PATH if not dev_env else OUTPUT_PATH_DEV, index=False, encoding="utf-8-sig")
    print("Completed data scrapping, extracting to csv")


def pipeline_scrape(dev_env = False):
    driver, wait = init_driver()
    scrape(driver, wait, dev_env)
    driver.quit()


if __name__ == "__main__":
    dev_env = len(sys.argv) > 1 and sys.argv[1] == "dev"
    driver, wait = init_driver(dev_env)
    scrape(driver, wait, dev_env)
    driver.quit()
