# 🚀 Data Pipeline Project

An end-to-end ETL data pipeline that automatically ingests, transforms, and stores data for analytics and reporting.

## 📌 Project Overview

This project simulates a real-world data engineering pipeline. It pulls data from a public dataset, cleans and transforms it using SQL, loads it into a PostgreSQL database, and visualizes insights through a dashboard — all automated and scheduled using Apache Airflow.

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Apache Airflow | Pipeline orchestration & scheduling |
| dbt | Data transformation using SQL |
| PostgreSQL | Data warehouse / storage |
| Docker | Containerization & environment setup |
| Python | Data ingestion scripts |
| Metabase | Dashboard & visualization |

## 🏗️ Architecture

Raw Data (API/CSV) → Python Ingestion → PostgreSQL (Raw) → dbt Transformation → PostgreSQL (Clean) → Dashboard

## 📂 Project Structure

data-pipeline-project/
├── dags/          # Airflow DAGs (pipeline schedules)
├── ingestion/     # Python scripts to fetch raw data
├── dbt/           # SQL transformation models
├── dashboard/     # Dashboard screenshots
└── docker-compose.yml  # Docker setup for Airflow

## 📊 Dataset

Chicago Crime Data (Public Dataset)
Source: Chicago Data Portal

## 🚧 Status

🔨 In Progress — actively being built
