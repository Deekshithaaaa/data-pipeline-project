# 🚀 Chicago Crime Analytics — End-to-End Data Pipeline

An automated end-to-end ETL data pipeline that ingests, transforms, and visualizes 
real Chicago crime data using modern data engineering tools.

## 📊 Dashboard
![Dashboard](dashboard/chicago_crime_dashboard.pdf)

**Key Insights:**
- 🔴 Battery is the #1 crime with 228 incidents
- 🟡 Theft follows closely with 198 incidents  
- 📈 Overall arrest rate is 17.81%
- 🚔 Narcotics has the highest arrest rate at 88%

## 🏗️ Architecture
Chicago Data Portal (API)
↓
Python Ingestion Script
↓
PostgreSQL (Raw Layer)
↓
SQL Transformations
↓
PostgreSQL (Clean Layer)
↓
Google Looker Studio Dashboard

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Apache Airflow | Pipeline orchestration & scheduling |
| PostgreSQL | Data warehouse |
| Docker | Containerization |
| Python | Data ingestion & transformation |
| SQL | Data transformation models |
| Google Looker Studio | Dashboard & visualization |

## 📂 Project Structure
data-pipeline-project/
├── dags/                    # Airflow DAGs
│   └── chicago_crimes_dag.py
├── ingestion/               # Python scripts
│   ├── ingest_chicago_crimes.py
│   └── transform.py
├── dbt/                     # SQL transformation models
│   └── chicago_crimes/
│       └── models/
├── dashboard/               # Dashboard files
│   ├── chicago_crime_dashboard.pdf
│   ├── crimes_by_type.csv
│   └── crimes_by_district.csv
└── docker-compose.yml

## 📊 Dataset
- **Source:** Chicago Data Portal (Public API)
- **Size:** 1,000+ daily crime records
- **URL:** https://data.cityofchicago.org/resource/ijzp-q8t2.json

## ⚙️ How to Run

### Prerequisites
- Docker Desktop
- Python 3.12+

### Steps
```bash
# Clone the repo
git clone https://github.com/Deekshithaaaa/data-pipeline-project.git
cd data-pipeline-project

# Start Airflow
docker-compose up -d

# Run ingestion
python ingestion/ingest_chicago_crimes.py

# Run transformations
python ingestion/transform.py
```

## 🔍 Key Findings
- **Battery** and **Theft** account for 42% of all crimes
- **Narcotics** has the highest arrest rate at 88%
- **Deceptive Practice** and **Robbery** have 0% arrest rate
- Most crimes occur in Districts 8, 11, and 6