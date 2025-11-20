from datetime import timedelta
import pendulum
from airflow.decorators import dag
from airflow.operators.dummy import DummyOperator

from operators.stage_redshift import StageToRedshiftOperator
from operators.load_fact import LoadFactOperator
from operators.load_dimension import LoadDimensionOperator
from operators.data_quality import DataQualityOperator

from helpers import SqlQueries


default_args = {
    "owner": "udacity",
    "depends_on_past": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "email_on_retry": False,
    "start_date": pendulum.datetime(2023, 1, 1),
}

@dag(
    default_args=default_args,
    description="Load and transform data in Redshift with Airflow",
    schedule_interval="0 * * * *",
    catchup=False,
)
def final_project():

    # -----------------------------------------------------
    # Start / End
    # -----------------------------------------------------
    start_operator = DummyOperator(task_id="Begin_execution")
    end_operator = DummyOperator(task_id="Stop_execution")

    # -----------------------------------------------------
    # Stage Events
    # -----------------------------------------------------
    stage_events_to_redshift = StageToRedshiftOperator(
        task_id="Stage_events",
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        table="staging_events",
        s3_bucket="airflow-project-nestr",
        s3_key="log-data",
        json_path="s3://airflow-project-nestr/log_json_path.json",
    )

    # -----------------------------------------------------
    # Stage Songs
    # -----------------------------------------------------
    stage_songs_to_redshift = StageToRedshiftOperator(
        task_id="Stage_songs",
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        table="staging_songs",
        s3_bucket="airflow-project-nestr",
        s3_key="song-data",
        json_path="auto",
    )

    # -----------------------------------------------------
    # Load Fact Table
    # -----------------------------------------------------
    load_songplays_table = LoadFactOperator(
        task_id="Load_songplays_fact_table",
        redshift_conn_id="redshift",
        table="songplays",
        sql_statement=SqlQueries.songplay_table_insert,
    )

    # -----------------------------------------------------
    # Load Dimension Tables
    # -----------------------------------------------------
    load_user_dimension_table = LoadDimensionOperator(
        task_id="Load_user_dim_table",
        redshift_conn_id="redshift",
        table="users",
        sql_statement=SqlQueries.user_table_insert,
        insert_mode="truncate",
    )

    load_song_dimension_table = LoadDimensionOperator(
        task_id="Load_song_dim_table",
        redshift_conn_id="redshift",
        table="songs",
        sql_statement=SqlQueries.song_table_insert,
        insert_mode="truncate",
    )

    load_artist_dimension_table = LoadDimensionOperator(
        task_id="Load_artist_dim_table",
        redshift_conn_id="redshift",
        table="artists",
        sql_statement=SqlQueries.artist_table_insert,
        insert_mode="truncate",
    )

    load_time_dimension_table = LoadDimensionOperator(
        task_id="Load_time_dim_table",
        redshift_conn_id="redshift",
        table="time",
        sql_statement=SqlQueries.time_table_insert,
        insert_mode="truncate",
    )

    # -----------------------------------------------------
    # Data Quality
    # -----------------------------------------------------
    run_quality_checks = DataQualityOperator(
        task_id="Run_data_quality_checks",
        redshift_conn_id="redshift",
        tests=[
            {"sql": "SELECT COUNT(*) FROM songplays;", "expected_operator": ">", "expected_value": 0},
            {"sql": "SELECT COUNT(*) FROM users;", "expected_operator": ">", "expected_value": 0},
            {"sql": "SELECT COUNT(*) FROM songs;", "expected_operator": ">", "expected_value": 0},
            {"sql": "SELECT COUNT(*) FROM artists;", "expected_operator": ">", "expected_value": 0},
            {"sql": "SELECT COUNT(*) FROM time;", "expected_operator": ">", "expected_value": 0},
        ],
    )

    # -----------------------------------------------------
    # Dependencies
    # -----------------------------------------------------

    # Start → staging
    start_operator >> [stage_events_to_redshift, stage_songs_to_redshift]

    # Both staging tasks → fact load
    [stage_events_to_redshift, stage_songs_to_redshift] >> load_songplays_table

    # Fact → all dimensions
    load_songplays_table >> [
        load_user_dimension_table,
        load_song_dimension_table,
        load_artist_dimension_table,
        load_time_dimension_table,
    ]

    # Dimensions → DQ → end
    [
        load_user_dimension_table,
        load_song_dimension_table,
        load_artist_dimension_table,
        load_time_dimension_table,
    ] >> run_quality_checks >> end_operator



final_project_dag = final_project()
