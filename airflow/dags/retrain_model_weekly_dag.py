from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys

sys.path.append('/opt/airflow/model')
from train_weather_model import train_and_save_model


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 1, 1),
    'retries': 3,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id='train_weather_model',
    default_args=default_args,
    schedule_interval='@weekly',
    catchup=False
) as dag:
    train_model_task = PythonOperator(
        task_id="train_model_task",
        python_callable=train_and_save_model
    )
