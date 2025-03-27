from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import pandas as pd
import psycopg2
import os

POSTGRES_CONN = {
    'host': 'postgres',
    'dbname': 'weatherdb',
    'user': 'airflow',
    'password': 'airflow'
}

def extract_weather_data():
    url = (
        "https://api.open-meteo.com/v1/forecast?"
        "latitude=10.762622&longitude=106.660172&hourly=temperature_2m,precipitation,cloudcover"
    )
    response = requests.get(url)
    data = response.json()

    df = pd.DataFrame({
        "timestamp": data["hourly"]["time"],
        "temperature": data["hourly"]["temperature_2m"],
        "precipitation": data["hourly"]["precipitation"],
        "cloudcover": data["hourly"]["cloudcover"],
    })

    conn = psycopg2.connect(**POSTGRES_CONN)
    cur = conn.cursor()
    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO raw_weather_data (timestamp, temperature, precipitation, cloudcover)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT DO NOTHING;
        """, (row["timestamp"], row["temperature"], row["precipitation"], row["cloudcover"]))
    conn.commit()
    cur.close()
    conn.close()

def transform_data():
    conn = psycopg2.connect(**POSTGRES_CONN)
    df = pd.read_sql("SELECT * FROM raw_weather_data", conn)
    df['is_raining'] = df['precipitation'] > 0.1
    df['is_cloudy'] = df['cloudcover'] > 50
    df = df[['timestamp', 'temperature', 'is_raining', 'is_cloudy']].rename(columns={"temperature": "temperature_celsius"})

    cur = conn.cursor()
    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO processed_weather_data (timestamp, temperature_celsius, is_raining, is_cloudy)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT DO NOTHING;
        """, (row["timestamp"], row["temperature_celsius"], row["is_raining"], row["is_cloudy"]))
    conn.commit()
    cur.close()
    conn.close()

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 3, 1),
    'retries': 2,
    'retry_delay': timedelta(minutes=3)
}

with DAG(
    dag_id='weather_elt_pipeline',
    default_args=default_args,
    schedule_interval='@hourly',
    catchup=False
) as dag:
    extract_task = PythonOperator(
        task_id='extract_weather_data',
        python_callable=extract_weather_data
    )

    transform_task = PythonOperator(
        task_id='transform_weather_data',
        python_callable=transform_data
    )

    extract_task >> transform_task
