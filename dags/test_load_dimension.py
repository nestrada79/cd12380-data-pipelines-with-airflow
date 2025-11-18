from airflow import DAG
from datetime import datetime
from airflow.operators.dummy import DummyOperator
from operators.load_dimension import LoadDimensionOperator
from helpers.sql_queries import SqlQueries

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 0
}

with DAG(
    'test_load_dimension',
    default_args=default_args,
    schedule_interval=None,
    catchup=False
) as dag:

    start = DummyOperator(task_id='start')

    load_users_dim = LoadDimensionOperator(
        task_id='load_users_dimension_test',
        redshift_conn_id='redshift',
        table='users',
        sql_statement=SqlQueries.user_table_insert,
        insert_mode="truncate"   # you can switch this to "append" later
    )

    end = DummyOperator(task_id='end')

    start >> load_users_dim >> end
