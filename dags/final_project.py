from datetime import timedelta
import pendulum
from airflow.decorators import dag
from airflow.operators.dummy import DummyOperator
from operators import StageToRedshiftOperator

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
    description='Load and transform data in Redshift with Airflow',
    schedule_interval='0 * * * *',
    catchup=False
)
def final_project():

    # Start / End
    start_operator = DummyOperator(task_id='Begin_execution')
    end_operator = DummyOperator(task_id='Stop_execution')

    # Stage_events only
    stage_events_to_redshift = StageToRedshiftOperator(
        task_id="Stage_events",
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        table="staging_events",
        s3_bucket="airflow-project-nestr",
        s3_key="log-data",
        json_path="s3://airflow-project-nestr/log_json_path.json",
    )

    start_operator >> stage_events_to_redshift >> end_operator


final_project_dag = final_project()
