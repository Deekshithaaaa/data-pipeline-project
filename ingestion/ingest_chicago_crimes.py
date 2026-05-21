import pandas as pd
import requests
from sqlalchemy import create_engine
import json

# ----------------------------------------
# STEP 1: Pull data from Chicago Data Portal
# ----------------------------------------
print("Fetching Chicago Crime data...")

url = "https://data.cityofchicago.org/resource/ijzp-q8t2.json"
params = {
    "$limit": 100000,
    "$order": "date DESC"
}

response = requests.get(url, params=params)
data = response.json()

df = pd.DataFrame(data)
print(f"Fetched {len(df)} rows of data!")

# ----------------------------------------
# STEP 2: Clean the data
# ----------------------------------------
print("Cleaning data...")

# Convert any dict/list columns to strings
for col in df.columns:
    if df[col].dtype == object:
        df[col] = df[col].apply(
            lambda x: json.dumps(x) if isinstance(x, (dict, list)) else x
        )

print(f"Columns: {list(df.columns)}")

# ----------------------------------------
# STEP 3: Connect to PostgreSQL
# ----------------------------------------
print("\nConnecting to PostgreSQL...")

engine = create_engine(
    "postgresql+psycopg2://airflow:airflow@localhost:5432/airflow"
)

# ----------------------------------------
# STEP 4: Load data into PostgreSQL
# ----------------------------------------
print("Loading data into database...")

df.to_sql(
    name="raw_chicago_crimes",
    con=engine,
    if_exists="replace",
    index=False
)

print("✅ Done! Data loaded into raw_chicago_crimes table!")