import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.extract_weather import extract_city_weather
from scripts.merge_weather import merge_weather

CITIES = ["paris", "tokyo", "barcelone", "montréal", "marrakesh"]

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime.datetime(2025, 6, 20),
    "retries": 10 
}

with DAG(
    "weather_etl_pipeline",
    default_args=default_args,
    schedule="@daily",
    catchup=False,
    max_active_runs=1,
) as dag:
    extract_tasks = [
        PythonOperator(
            task_id=f"extract_{city.lower()}",
            python_callable=extract_city_weather,
            op_args=[city, datetime.datetime.now(), "{{var.value.WEATHER_API_KEY}}"],
        )
        for city in CITIES
    ]

    merge_task = PythonOperator(
        task_id=f"merge_weather",
        python_callable=merge_weather,
        op_args=["{{ds}}"]
    )

    extract_tasks >> merge_task
