from datetime import datetime, timedelta

def get_closest_past_thursday():
    today = datetime.now()
    days_to_thursday = (today.weekday() - 3) % 7  # Calculate days to the closest past Friday
    thursday_date = today - timedelta(days=days_to_thursday)
    return thursday_date.strftime("%Y-%m-%d")

def create_urls(dev_env=False):

    countries_file_path = "./countries_lists/countries.txt"
    if dev_env:
        countries_file_path = "./countries_lists/countries_test.txt"

    with open(countries_file_path, "r") as countries:
        lines = countries.readlines()
        countries = [i.split(",")[0].strip() for i in lines]
        countries_short = [i.split(",")[-1].strip() for i in lines]

        # Create urls based on short version of country name
        urls = [
            "https://charts.spotify.com/charts/view/regional-" + s + "-weekly/latest"
            for s in countries_short
        ]

        return zip(countries, countries_short, urls)


if __name__ == "__main__":
    create_urls(True)
