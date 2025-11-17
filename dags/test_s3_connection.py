from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from datetime import datetime

BUCKET_NAME = "airflow-project-nestr"  

def test_s3():
    hook = S3Hook(aws_conn_id="aws_credentials")
    try:
        objects = hook.list_keys(bucket_name=BUCKET_NAME)
        if objects:
            print(f"S3 connection OK. Found {len(objects)} keys.")
        else:
            print("S3 connection OK but bucket is empty.")
    except Exception as e:
        print("S3 connection failed.")
        print(str(e))
        raise

with DAG(
    dag_id="test_s3_connection",
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,
    catchup=False
) as dag:

    test_s3_task = PythonOperator(
        task_id="test_s3_task",
        python_callable=test_s3
    )
