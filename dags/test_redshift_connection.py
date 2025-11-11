from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from datetime import datetime

def test_redshift_connection():
    try:
        hook = PostgresHook(postgres_conn_id='redshift')
        conn = hook.get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT 1;")
        result = cursor.fetchone()
        print("✅ Redshift connection successful, result:", result)
        conn.close()
    except Exception as e:
        print("❌ Redshift connection failed:", str(e))
        raise

with DAG(
    dag_id='test_redshift_connection',
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=['test', 'connection'],
) as dag:
    test_connection = PythonOperator(
        task_id='check_redshift_connection',
        python_callable=test_redshift_connection
    )
