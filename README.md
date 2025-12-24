# E-Commerce Data Engineering Pipeline

**Student Name:** JAI DURGA VAISHANAVI KOLA  
**Roll Number:** 23A91A6126  
**Submission Date:** December 2025  

---

## 📌 Project Overview

This project implements an **end-to-end ETL data engineering pipeline** for an e-commerce analytics platform.  
It covers the complete lifecycle of data engineering including synthetic data generation, ingestion, data quality validation, transformation across schemas, dimensional data warehousing, automated testing, orchestration, and business intelligence using Power BI.

The project follows **industry best practices** such as layered database architecture, star schema modeling, and analytics-ready reporting.

---

## 🏗️ Pipeline Architecture

Data flows through the following stages:

1. **Data Generation** (Synthetic CSV files)
2. **Data Ingestion → Staging Schema**
3. **Data Quality Checks**
4. **Staging → Production Transformation**
5. **Warehouse Load (Dimensional Star Schema)**
6. **Analytics-Ready Data**
7. **Power BI Dashboard Visualization**

---

## 🛠️ Prerequisites

- Python 3.9+
- PostgreSQL 14+
- Docker & Docker Compose
- Git
- Power BI Desktop (Free)

---

## ⚙️ Installation & Setup

### Clone the repository and install dependencies:

```bash
git clone https://github.com/KolaVaishnavi294/ecommerce-data-pipeline-23A91A6126.git
cd ecommerce-data-pipeline-23A91A6126
pip install -r requirements.txt
```
### Start PostgreSQL using Docker:
```bash
docker-compose up -d
```
### Verify database container:

```bash
docker ps
```
### Database Configuration

- Database Name: ecommerce_db

#### Schemas Used:

- staging – Raw ingested data

- production – Cleaned and normalized data

- warehouse – Dimensional star schema for analytics

### Running the Pipeline
Run the entire pipeline using a single command:

```bash
python scripts/orchestration/pipeline_runner.py
```
This executes:

- Data generation

- Staging ingestion

- Data quality validation

- Production transformation

- Warehouse loading

### Run data quality checks only:

```bash
python scripts/quality_checks/validate_data.py
```
## ⏱️ Orchestration & Automation

- Centralized pipeline orchestration using Python

- Step-wise execution with logging and retries

- Designed as a full-refresh batch pipeline

- Windows-compatible logging (emoji-free)

Logs are generated in:

```bash
logs/pipeline.log
```
## 📊 Power BI Dashboard

Power BI Desktop is used as the analytics and visualization layer, connected directly to the PostgreSQL warehouse schema.

### Dashboard Pages (4 Pages):
- Executive Overview

- Product Performance

- Customer Analytics

- Trends & Geography

### Dashboard Features:

- KPIs: Revenue, Profit, Transactions

- Interactive slicers: Date, Category, State, Payment Method

- Star schema data model

- Multiple charts, maps, and tables for insights

### Power BI Files:
```bash
dashboards/powerbi/
├── ecommerce_analytics.pbix
├── dashboard_export.pdf
└── dashboard_metadata.json
```
Screenshots of all dashboard pages are available in:

```bash
dashboards/screenshots/
```
## 🧪 Testing & Validation
Automated unit tests are implemented using PyTest.

Run all tests:

```bash
python -m pytest tests/ -v
```
### Tests validate:

- Data generation accuracy

- Referential integrity

- Data quality rules

- Production transformations

- Warehouse fact and dimension tables

All tests pass successfully.


# ✅ Conclusion
This project demonstrates a complete, production-style data engineering pipeline with structured ETL layers, data quality assurance, automated testing, orchestration, and business intelligence dashboards.
