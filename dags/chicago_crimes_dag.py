from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import requests
from sqlalchemy import create_engine, text
import json
import sys

default_args = {
    'owner': 'deekshitha',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'email': ['deek0811@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
}

def ingest_chicago_crimes():
    print("Fetching Chicago Crime data...")
    url = "https://data.cityofchicago.org/resource/ijzp-q8t2.json"
    params = {"$limit": 100000, "$order": "date DESC"}
    response = requests.get(url, params=params)
    data = response.json()
    df = pd.DataFrame(data)
    print(f"Fetched {len(df)} rows!")
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].apply(
                lambda x: json.dumps(x) if isinstance(x, (dict, list)) else x
            )
    engine = create_engine(
        "postgresql+psycopg2://airflow:airflow@postgres/airflow"
    )
    df.to_sql(
        name="raw_chicago_crimes",
        con=engine,
        if_exists="replace",
        index=False
    )
    print("✅ Ingestion done!")

def run_transformations():
    print("Running transformations...")
    engine = create_engine(
        "postgresql+psycopg2://airflow:airflow@postgres/airflow"
    )
    with engine.begin() as conn:
        conn.execute(text("""
            DROP TABLE IF EXISTS stg_chicago_crimes;
            CREATE TABLE stg_chicago_crimes AS
            SELECT
                id, case_number, date::timestamp AS crime_date,
                block, primary_type AS crime_type, description,
                location_description, arrest::boolean AS was_arrested,
                domestic::boolean AS is_domestic, beat, district,
                ward, community_area, year::integer AS crime_year,
                latitude::float AS latitude, longitude::float AS longitude
            FROM raw_chicago_crimes
            WHERE id IS NOT NULL AND date IS NOT NULL;
        """))
        conn.execute(text("""
            DROP TABLE IF EXISTS crimes_by_type;
            CREATE TABLE crimes_by_type AS
            SELECT
                crime_type, COUNT(*) AS total_crimes,
                SUM(CASE WHEN was_arrested THEN 1 ELSE 0 END) AS total_arrests,
                ROUND(100.0 * SUM(CASE WHEN was_arrested THEN 1 ELSE 0 END) / COUNT(*), 2) AS arrest_rate_pct
            FROM stg_chicago_crimes
            GROUP BY crime_type ORDER BY total_crimes DESC;
        """))
        conn.execute(text("""
            DROP TABLE IF EXISTS crimes_by_district;
            CREATE TABLE crimes_by_district AS
            SELECT
                district, COUNT(*) AS total_crimes,
                SUM(CASE WHEN was_arrested THEN 1 ELSE 0 END) AS total_arrests,
                ROUND(100.0 * SUM(CASE WHEN was_arrested THEN 1 ELSE 0 END) / COUNT(*), 2) AS arrest_rate_pct,
                COUNT(DISTINCT crime_type) AS unique_crime_types
            FROM stg_chicago_crimes
            GROUP BY district ORDER BY total_crimes DESC;
        """))
    print("✅ Transformations done!")

def run_quality_checks():
    print("Running quality checks...")
    engine = create_engine(
        "postgresql+psycopg2://airflow:airflow@postgres/airflow"
    )
    with engine.connect() as conn:
        count = conn.execute(text(
            "SELECT COUNT(*) FROM raw_chicago_crimes"
        )).scalar()
        if count < 50000:
            raise ValueError(f"❌ Row count too low: {count}")
        null_ids = conn.execute(text(
            "SELECT COUNT(*) FROM raw_chicago_crimes WHERE id IS NULL"
        )).scalar()
        if null_ids > 0:
            raise ValueError(f"❌ Found {null_ids} null IDs!")
    print(f"✅ Quality checks passed! {count:,} records found.")

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

    transform_task = PythonOperator(
        task_id="run_transformations",
        python_callable=run_transformations,
    )

    quality_task = PythonOperator(
        task_id="run_quality_checks",
        python_callable=run_quality_checks,
    )

    ingest_task >> transform_task >> quality_task