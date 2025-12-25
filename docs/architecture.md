# E-Commerce Data Pipeline Architecture

## Overview
This project implements an end-to-end data engineering pipeline for an e-commerce analytics platform.  
The pipeline follows a layered architecture that separates raw data ingestion, cleansed operational data, and analytical data models to ensure scalability, data quality, and analytical performance.

The overall data flow is:

Raw CSV Data → Staging Schema → Production Schema → Warehouse Schema → Analytics & Dashboard

---

## Three-Tier Schema Design

### 1. Staging Schema
The staging layer acts as a raw landing zone for generated CSV data.  
It mirrors the source data structure exactly and applies minimal constraints to support fast and reliable bulk loading.

**Purpose:**
- Fast ingestion of raw data
- Preserve source data without modification
- Enable reprocessing and debugging if issues occur

**Characteristics:**
- Minimal constraints
- No complex business logic
- Temporary storage layer

---

### 2. Production Schema
The production layer stores cleansed, validated, and normalized data following third normal form (3NF).

**Purpose:**
- Enforce data integrity and business rules
- Serve as a trusted operational data layer
- Eliminate duplicates, inconsistencies, and invalid records

**Key Features:**
- Primary and foreign key constraints
- Unique constraints (e.g., customer email)
- Cleaned and standardized fields
- Idempotent loading logic

---

### 3. Warehouse Schema
The warehouse layer is designed specifically for analytics and reporting using a dimensional (star) schema.

**Purpose:**
- Enable fast analytical queries
- Support business intelligence tools
- Separate analytical workloads from operational processing

**Design Approach:**
- Central fact table for sales transactions
- Surrounding dimension tables for descriptive attributes
- Pre-aggregated tables for performance optimization

---

## Star Schema Rationale
A star schema is used in the warehouse because it:
- Simplifies analytical queries
- Reduces complex joins
- Improves query performance
- Aligns with industry-standard BI practices

Fact tables store measurable business events, while dimension tables provide descriptive context such as customer, product, date, and payment method.

---

## Slowly Changing Dimension (SCD) Type 2
SCD Type 2 is implemented for customer and product dimensions to track historical changes over time.

**Why SCD Type 2 is required:**
- Customers and products can change attributes (location, price category, etc.)
- Business analysis often requires historical accuracy
- Enables time-based analysis and trend comparison

**How it works:**
- Each change creates a new dimension record
- Previous records are expired using end_date
- The current record is marked using is_current = true

This approach preserves historical context while maintaining accurate current-state reporting.

---

## Conclusion
The layered architecture ensures:
- Data reliability through separation of concerns
- Scalability for growing data volumes
- Accurate and performant analytics

This design reflects real-world data engineering best practices used in production analytics systems.
