.PHONY: help setup run ingest transform quality stop clean

help:
	@echo "Chicago Crime Data Pipeline"
	@echo "=========================="
	@echo "make setup    - Start Docker containers"
	@echo "make run      - Run full pipeline"
	@echo "make ingest   - Run ingestion only"
	@echo "make transform - Run transformations only"
	@echo "make quality  - Run quality checks only"
	@echo "make stop     - Stop Docker containers"
	@echo "make clean    - Stop and remove containers"

setup:
	docker-compose up -d
	@echo "✅ Airflow is running at http://localhost:8080"

ingest:
	python ingestion/ingest_chicago_crimes.py

transform:
	python ingestion/transform.py

quality:
	python ingestion/data_quality.py

run: ingest transform quality
	@echo "🎉 Full pipeline completed!"

stop:
	docker-compose down

clean:
	docker-compose down -v
	@echo "✅ All containers removed!"