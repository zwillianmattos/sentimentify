from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

import sys
sys.path.append('/usr/src/app')

from extractors.twitter_extractor import TwitterExtractor
from transformers.sentiment_analyzer import SentimentAnalyzer
from loaders.postgres_loader import PostgresLoader
import pandas as pd

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def extract_data(**context):
    twitter = TwitterExtractor()
    mentions = twitter.extract_mentions("your_brand_name")
    if mentions:
        return mentions
    return []

def transform_data(**context):
    mentions = context['task_instance'].xcom_pull(task_ids='extract_task')
    if mentions:
        mentions_df = pd.DataFrame(mentions)
        analyzer = SentimentAnalyzer()
        analyzed_df = analyzer.analyze_texts(mentions_df)
        return analyzed_df.to_dict('records')
    return []

def load_data(**context):
    analyzed_data = context['task_instance'].xcom_pull(task_ids='transform_task')
    if analyzed_data:
        df = pd.DataFrame(analyzed_data)
        loader = PostgresLoader()
        loader.load_data(df, 'social_mentions')

with DAG(
    'sentiment_analysis_etl',
    default_args=default_args,
    description='Sentiment Analysis ETL pipeline',
    schedule_interval=timedelta(minutes=5),
    start_date=days_ago(1),
    catchup=False,
    tags=['sentiment_analysis'],
) as dag:

    extract_task = PythonOperator(
        task_id='extract_task',
        python_callable=extract_data,
    )

    transform_task = PythonOperator(
        task_id='transform_task',
        python_callable=transform_data,
    )

    load_task = PythonOperator(
        task_id='load_task',
        python_callable=load_data,
    )

    extract_task >> transform_task >> load_task 