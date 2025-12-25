# Project Submission

## Student Information
- **Student Name:** JAI DURGA VAISHANAVI KOLA  
- **Roll Number:** 23A91A6126 
- **Submission Date:** December 2025  

---

## GitHub Repository
- **Repository URL:**  
  https://github.com/KolaVaishnavi294/ecommerce-data-pipeline-23A91A6126

---

## Project Objective
The objective of this project is to build an end-to-end data engineering pipeline for an e-commerce analytics platform.  
The pipeline demonstrates data generation, ingestion, data quality validation, schema-based transformations, dimensional data warehousing, orchestration, and business intelligence reporting using Power BI.

---

## Phase-wise Implementation Overview

### Phase 1: Project Setup & Environment Configuration
- Repository initialized with required folder structure
- Environment setup documented
- Dependencies managed using `requirements.txt`
- Docker and Docker Compose configuration included
- Database schemas defined and organized

---

### Phase 2: Data Generation & Ingestion
- Synthetic e-commerce data generated using Python
- CSV files created for customers, products, transactions, and transaction items
- Referential integrity maintained with zero orphan records
- Data ingested into PostgreSQL staging schema
- Ingestion summary generated in JSON format

---

### Phase 3: Data Quality, Transformation & Warehouse
- Data quality checks implemented (nulls, duplicates, ranges, referential integrity)
- Quality report generated with overall quality score
- Data transformed from staging to production schema
- Business rules applied during transformation
- Dimensional warehouse created using star schema
- SCD Type 2 implemented for customer and product dimensions
- Aggregate tables generated for analytics performance

---

### Phase 4: Analytics & Business Intelligence
- Analytical SQL queries executed on warehouse schema
- Analytics-ready datasets produced
- Power BI dashboard created with four pages:
  - Executive Overview
  - Product Performance
  - Customer Analytics
  - Trends & Geography
- Interactive KPIs, slicers, and visual insights implemented
- Dashboard screenshots included in the repository

---

### Phase 5: Pipeline Automation & Orchestration
- Python-based pipeline orchestration implemented
- Step-wise execution with retries and logging
- End-to-end pipeline execution verified
- Execution logs generated
- Pipeline execution summary documented in JSON format

---

### Phase 6: Testing & Documentation
- Unit tests written using PyTest
- Tests validate data generation, ingestion, quality checks, and transformations
- Documentation added for:
  - Architecture
  - Dashboard usage
  - Pipeline execution
- README updated with complete setup and usage instructions

---

### Phase 7: Deployment & Submission
- Docker-based deployment configuration included
- Repository finalized for submission
- Version-controlled codebase with all required artifacts

---

## Dashboard Artifacts
- **Power BI File:** `dashboards/powerbi/ecommerce_analytics.pbix`
- **Dashboard Screenshots:** `dashboards/screenshots/`
- **Dashboard Metadata:** `dashboards/powerbi/dashboard_metadata.json`

---

## Key Deliverables Summary
- End-to-end ETL pipeline (Python + PostgreSQL)
- Three-tier database architecture (staging, production, warehouse)
- Dimensional data warehouse with SCD Type 2
- Data quality validation and reporting
- Automated pipeline orchestration
- Power BI dashboard with business insights
- Unit tests and technical documentation

---

## Running Instructions

### Install dependencies
```bash
pip install -r requirements.txt
```
### Start database using Docker
```bash
docker-compose up -d
```
### Run full pipeline
```bash
python scripts/orchestration/pipeline_runner.py
```
### Run tests
```bash
pytest tests/ -v
```

---

## Project Statistics
- Total Records Generated: 30,000+

- Database Schemas: 3 (staging, production, warehouse)

- Warehouse Tables: Dimension tables, fact tables, and aggregate tables

- Dashboard Pages: 4

- Total Visualizations: 16+

---

## Challenges Faced & Solutions
- Unicode logging issues on Windows:
Resolved by removing non-ASCII characters from logging and console output to ensure Windows compatibility.

- Duplicate key conflicts during production loads:
Handled through idempotent loading logic and proper primary key constraints.

- Power BI connectivity challenges:
Resolved by validating warehouse schema relationships and configuring the Power BI data model correctly.

- Pipeline stability:
Improved by implementing retry logic and structured logging in the pipeline orchestration layer.

---

## Declaration
I hereby declare that this project is my original work and has been completed independently as part of the assigned task.