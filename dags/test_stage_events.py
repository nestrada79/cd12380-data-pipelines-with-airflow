from airflow import DAG
from datetime import datetime
from airflow.operators.dummy import DummyOperator
from operators.stage_redshift import StageToRedshiftOperator

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 0
}

with DAG(
    'test_stage_events',
    default_args=default_args,
    schedule_interval=None,
    catchup=False
) as dag:

    start = DummyOperator(task_id='start')

    stage_events = StageToRedshiftOperator(
        task_id='stage_events',
        table='staging_events',
        s3_bucket='airflow-project-nestr',
        s3_key='log-data',
        json_path='s3://airflow-project-nestr/log_json_path.json'
    )

    start >> stage_events
