from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import requests
from sqlalchemy import create_engine
import json

# ----------------------------------------
# Default settings for the DAG
# ----------------------------------------
default_args = {
    'owner': 'deekshitha',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# ----------------------------------------
# The function Airflow will run
# ----------------------------------------
def ingest_chicago_crimes():
    print("Fetching Chicago Crime data...")

    url = "https://data.cityofchicago.org/resource/ijzp-q8t2.json"
    params = {
        "$limit": 1000,
        "$order": "date DESC"
    }

    response = requests.get(url, params=params)
    data = response.json()
    df = pd.DataFrame(data)

    print(f"Fetched {len(df)} rows!")

    # Clean dict/list columns
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].apply(
                lambda x: json.dumps(x) if isinstance(x, (dict, list)) else x
            )

    # Connect to PostgreSQL
    engine = create_engine(
        "postgresql+psycopg2://airflow:airflow@postgres/airflow"
    )

    # Load into database
    df.to_sql(
        name="raw_chicago_crimes",
        con=engine,
        if_exists="replace",
        index=False
    )

    print("✅ Data loaded successfully!")

# ----------------------------------------
# Define the DAG
# ----------------------------------------
with DAG(
    dag_id="chicago_crimes_ingestion",
    default_args=default_args,
    description="Daily ingestion of Chicago Crime data",
    schedule_interval="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["chicago", "crimes", "ingestion"],
) as dag:

    ingest_task = PythonOperator(
        task_id="ingest_chicago_crimes",
        python_callable=ingest_chicago_crimes,
    )

    ingest_task