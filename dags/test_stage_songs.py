from airflow import DAG
from datetime import datetime
from operators.stage_redshift import StageToRedshiftOperator
from airflow.operators.dummy import DummyOperator

default_args = {
    "owner": "airflow",
    "start_date": datetime(2023, 1, 1),
    "retries": 0,
}

with DAG(
    "test_stage_songs",
    default_args=default_args,
    description="Test staging song_data to Redshift",
    schedule_interval=None,
    catchup=False,
) as dag:

    start = DummyOperator(task_id="start")

    stage_songs = StageToRedshiftOperator(
        task_id="stage_songs",
        table="staging_songs",
        s3_bucket="airflow-project-nestr",
        s3_key="song-data/",
        json_path="s3://airflow-project-nestr/song_json_path.json"

    )

    start >> stage_songs
