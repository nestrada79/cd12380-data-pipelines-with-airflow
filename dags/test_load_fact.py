from airflow import DAG
from datetime import datetime
from airflow.operators.dummy import DummyOperator
from operators.load_fact import LoadFactOperator
from helpers.sql_queries import SqlQueries


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 0
}

with DAG(
    'test_load_fact',
    default_args=default_args,
    schedule_interval=None,
    catchup=False
) as dag:

    start = DummyOperator(task_id='start')

    load_fact = LoadFactOperator(
        task_id='load_songplays_fact_test',
        redshift_conn_id='redshift',
        table='songplays',
        sql=SqlQueries.songplay_table_insert
    )

    end = DummyOperator(task_id='end')

    start >> load_fact >> end
