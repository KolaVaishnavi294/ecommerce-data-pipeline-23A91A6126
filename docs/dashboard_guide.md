# Power BI Dashboard Guide

## Overview

This document describes the Power BI dashboard created for the **E-Commerce Data Engineering Pipeline** project.  
The dashboard is built using **Power BI Desktop** and connected directly to the **PostgreSQL warehouse schema**.  
It provides business-ready insights using a star schema data model and supports interactive analysis through slicers and filters.

The dashboard consists of **four pages**:
1. Executive Overview  
2. Product Performance  
3. Customer Analytics  
4. Trends & Geography  

---

## Data Model

- **Fact Table**
  - `warehouse.fact_sales`
- **Dimension Tables**
  - `warehouse.dim_date`
  - `warehouse.dim_products`
  - `warehouse.dim_customers`
  - `warehouse.dim_payment_method`

The model follows a **star schema**, ensuring:
- Fast query performance
- Simple relationships
- Easy slicing and filtering across dimensions

---

## Global Filters & Slicers

The following slicers are available across dashboard pages:
- **Year / Quarter / Month / Day**
- **Category**
- **State**
- **Payment Method**
- **Transaction ID** (where applicable)

These slicers allow users to dynamically filter visuals and drill into specific subsets of data.

---

## Page 1: Executive Overview

### Purpose
Provides a high-level summary of overall business performance for executives and decision-makers.

### Key KPIs
- **Total Revenue (Sum of line_total)**
- **Transaction Count**
- **Revenue by Category**
- **Revenue by Payment Method**

### Visuals
- KPI Card showing total revenue
- Bar chart for **Top Categories by Revenue**
- Donut chart for **Payment Method Distribution**
- Filled map showing **Sales by Region**
- Line chart displaying **Monthly Revenue Trend**
- Transaction list for detailed inspection

### Insights Enabled
- Identify top-performing categories
- Understand preferred payment methods
- Analyze geographic revenue distribution
- Track revenue trends over time

---

## Page 2: Product Performance

### Purpose
Analyzes product-level performance and profitability.

### Visuals
- Horizontal bar chart showing **Top Products by Revenue**
- Matrix table with:
  - Product Name
  - Total Revenue
  - Total Profit
  - Quantity Sold
- Treemap showing **Revenue by Category and Brand**
- Scatter plot showing **Unit Price vs Profit**

### Insights Enabled
- Identify best-selling and most profitable products
- Compare category-level contribution
- Detect pricing vs profitability patterns
- Analyze product mix effectiveness

---

## Page 3: Customer Analytics

### Purpose
Focuses on customer behavior, segmentation, and revenue contribution.

### Visuals
- Bar chart showing **Revenue by Customer Segment**
- Area chart for **Revenue by Customer (Top Customers)**
- Stacked column chart showing **Monthly Revenue by Customer Segment**
- Tabular view of customer activity with date granularity

### Insights Enabled
- Compare revenue across customer segments (Young, Mid-age, Senior)
- Identify high-value customers
- Understand seasonal purchasing behavior
- Analyze customer contribution over time

---

## Page 4: Trends & Geography

### Purpose
Examines temporal trends and geographic sales performance.

### Visuals
- Line chart showing **Revenue by Day of Week**
- Bar chart showing **Top States by Revenue**
- Stacked area chart showing **Monthly Revenue by Category**
- Filled geographic map showing **State-wise Sales Distribution**

### Insights Enabled
- Identify peak sales days
- Compare regional performance
- Track category trends over months
- Support regional and time-based business decisions

---

## Dashboard Files

- **Power BI File:**  
  `dashboards/powerbi/ecommerce_analytics.pbix`

- **Screenshots:**  
  `dashboards/screenshots/`
  - `executive_overview.png`
  - `product_performance.png`
  - `customer_analytics.png`
  - `trends_geography.png`

- **Metadata:**  
  `dashboards/powerbi/dashboard_metadata.json`

---

## Conclusion

This Power BI dashboard transforms warehouse data into actionable business insights.  
By combining a clean star schema, interactive visuals, and meaningful KPIs, the dashboard supports both high-level decision-making and detailed analytical exploration.
