from datetime import datetime
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from operators.data_quality import DataQualityOperator

default_args = {
    "owner": "airflow",
    "start_date": datetime(2023, 1, 1),
    "retries": 0,
}

with DAG(
    "test_data_quality",
    default_args=default_args,
    description="Test DataQualityOperator against Redshift",
    schedule_interval=None,
    catchup=False,
) as dag:

    start = DummyOperator(task_id="start")

    dq_checks = DataQualityOperator(
        task_id="run_dq_checks",
        redshift_conn_id="redshift",
        tests=[
            {
                "sql": "SELECT COUNT(*) FROM songplays;",
                "expected_result": lambda x: x > 0,  # expect non-zero
            },
            {
                "sql": "SELECT COUNT(*) FROM users;",
                "expected_result": lambda x: x > 0,  # expect non-zero
            },
        ],
    )

    start >> dq_checks

