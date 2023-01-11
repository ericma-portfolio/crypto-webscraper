import sys
import os
sys.path.insert(0,os.path.abspath(os.path.dirname('/Users/ericma/desktop/cryptoScraper/dags/scripts')))
import scripts.get_price as get_price
import pandas as pd
from io import StringIO
import boto3
from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

data = get_price.get_price()

coin_data = {
    'symbol' : [data[0][0], data[1][0], data[2][0], data[3][0], data[4][0], data[5][0], data[6][0], data[7][0], data[8][0], data[9][0]],
    'price' : [data[0][1], data[1][1], data[2][1], data[3][1], data[4][1], data[5][1], data[6][1], data[7][1], data[8][1], data[9][1]]
}

def upload_to_s3() :
    df = pd.DataFrame(coin_data)
    bucket = 'crypto-webscraper'
    csv_buffer = StringIO()
    df.to_csv(csv_buffer)
    s3_resource = boto3.resource('s3', aws_access_key_id = os.getenv('S3_ACCESS_KEY_ID'), aws_secret_access_key = os.getenv('S3_SECRET_ACCESS_KEY'))
    s3_resource.Object(bucket, 'testv3.csv').put(Body=csv_buffer.getvalue())

default_args = {
    'owner' : 'Eric',
    'retries' : 5,
    'retry_delay' : timedelta(minutes = 5)
}

with DAG(
    default_args = default_args,
    dag_id = 'upload_to_s3',
    description = 'Upload top 10 coins to s3 daily',
    start_date = datetime(2023 , 1, 11),
    schedule_interval = '@daily'
) as dag:
    task1 = PythonOperator(
        task_id = 'upload_to_s3',
        python_callable = upload_to_s3,
    )
    
    task1
