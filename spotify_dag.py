from datetime import datetime, timedelta
from textwrap import dedent 

from airflow import DAG

from airflow.operators.python_operator import PythonOperator

from src.scraper.scraper import pipeline_scrape
from src.features.features import pipeline_features
from src.create_database import create_database
from src.persistence.persistence import pipeline_persistence

with DAG(
    'spotify_dag',
    default_args={
        'depends_on_past': False,
        'email': ['airflow@example.com'],
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 4,
        'retry_delay': timedelta(minutes=10),
        'execution_timeout': timedelta(minutes=10)
    },
    description='DAG to pull data from the Spotify API',
    schedule_interval=timedelta(days=7),
    start_date=datetime(2023, 1, 1),
    tags=['spotify'],
) as dag:
    
    t1 = PythonOperator(
            task_id='extract_data',
            python_callable=pipeline_scrape,
            dag=dag)
    t2 = PythonOperator(
            task_id='add_features',
            python_callable=pipeline_features,
            dag=dag)
    t3 = PythonOperator(
            task_id='create_database',
            python_callable=create_database,
            dag=dag)
    t4 = PythonOperator(
            task_id='persist_data',
            python_callable=pipeline_persistence,
            dag=dag)

    t1 >> t2 >> t3 >> t4