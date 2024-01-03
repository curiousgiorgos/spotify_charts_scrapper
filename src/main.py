# This script can be used to run the steps without Apache Airflow 
# Note the development database will always be create (if it doesn't exist!) 
# regardless of development mode or not

from scrapper.scrapper import pipeline_scrape
from features.features import pipeline_features
from create_database import create_database
from persistence.persistence import pipeline_persistence
import sys

sys.path.append('./scrapper')

if __name__=="__main__":
    dev_env = len(sys.argv) > 1 and sys.argv[1] == "dev"
    # step 1 - scrape data
    pipeline_scrape(dev_env)
    # step 2 - add features
    pipeline_features(dev_env)
    # step 3 - create database 
    create_database()
    # step 4 - add to database 
    pipeline_persistence(dev_env)