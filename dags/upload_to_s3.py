import os
import sys
from datetime import datetime
from io import StringIO

from airflow import DAG
from airflow.decorators import task
# from airflow.operators.python import PythonOperator
from dotenv import find_dotenv, load_dotenv

sys.path.insert(
    0,
    os.path.abspath(
        os.path.dirname("/Users/ericma/desktop/cryptoScraper/dags/scripts")
    ),
)

load_dotenv(find_dotenv())

# default_args = {"owner": "Eric", "retries": 1, "retry_delay": timedelta(minutes=5)}

with DAG(
    # default_args=default_args,
    dag_id="upload_to_s3",
    description="Upload top 10 coins to s3 daily",
    # start date 1-11-2023
    start_date=datetime(year=2023, month=1, day=16),
    # execute dag at 12:30 PM everyday, 18:30 UTC is 12:30 PM CENTRAL
    schedule_interval="30 18 * * *",
) as dag:

    @task()
    def upload_to_s3():
        from datetime import datetime

        import boto3
        import pandas as pd
        import scripts.get_price as get_price

        data = get_price.get_price()

        coin_data = {
            "symbol": [
                data[0][0],
                data[1][0],
                data[2][0],
                data[3][0],
                data[4][0],
                data[5][0],
                data[6][0],
                data[7][0],
                data[8][0],
                data[9][0],
            ],
            "price": [
                data[0][1],
                data[1][1],
                data[2][1],
                data[3][1],
                data[4][1],
                data[5][1],
                data[6][1],
                data[7][1],
                data[8][1],
                data[9][1],
            ],
        }

        df = pd.DataFrame(coin_data)
        bucket = "crypto-webscraper"
        csv_buffer = StringIO()
        df.to_csv(csv_buffer)
        s3_resource = boto3.resource(
            "s3",
            aws_access_key_id=os.getenv("S3_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("S3_SECRET_ACCESS_KEY"),
        )
        s3_resource.Object(
            bucket, "coin_data_{0}.csv".format(datetime.now().strftime("%Y-%m-%d"))
        ).put(Body=csv_buffer.getvalue())

    upload_to_s3()
    # task1 = PythonOperator(
    #    task_id="upload_to_s3",
    #    python_callable=upload_to_s3,
    # )
    # task1
