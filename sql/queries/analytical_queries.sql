-- 1. Top 10 Products by Revenue
SELECT
    p.product_name,
    p.category,
    SUM(f.line_total) AS total_revenue,
    SUM(f.quantity) AS units_sold
FROM warehouse.fact_sales f
JOIN warehouse.dim_products p
    ON f.product_key = p.product_key
GROUP BY p.product_name, p.category
ORDER BY total_revenue DESC
LIMIT 10;

-- 2. Monthly Sales Trend
SELECT
    d.year,
    d.month,
    SUM(f.line_total) AS monthly_revenue,
    COUNT(DISTINCT f.transaction_id) AS total_transactions
FROM warehouse.fact_sales f
JOIN warehouse.dim_date d
    ON f.date_key = d.date_key
GROUP BY d.year, d.month
ORDER BY d.year, d.month;

-- 3. Customer Segmentation by Spend
SELECT
    CASE
        WHEN SUM(f.line_total) < 1000 THEN 'Low'
        WHEN SUM(f.line_total) BETWEEN 1000 AND 5000 THEN 'Medium'
        ELSE 'High'
    END AS customer_segment,
    COUNT(DISTINCT f.customer_key) AS customer_count,
    SUM(f.line_total) AS total_revenue
FROM warehouse.fact_sales f
GROUP BY customer_segment;

-- 4. Category Performance
SELECT
    p.category,
    SUM(f.line_total) AS revenue,
    SUM(f.profit) AS total_profit
FROM warehouse.fact_sales f
JOIN warehouse.dim_products p
    ON f.product_key = p.product_key
GROUP BY p.category
ORDER BY revenue DESC;

-- 5. Payment Method Distribution
SELECT
    pm.payment_method_name,
    COUNT(*) AS transaction_count,
    SUM(f.line_total) AS revenue
FROM warehouse.fact_sales f
JOIN warehouse.dim_payment_method pm
    ON f.payment_method_key = pm.payment_method_key
GROUP BY pm.payment_method_name;

-- 6. Geographic Revenue Analysis
SELECT
    c.state,
    SUM(f.line_total) AS total_revenue,
    COUNT(DISTINCT f.customer_key) AS customers
FROM warehouse.fact_sales f
JOIN warehouse.dim_customers c
    ON f.customer_key = c.customer_key
GROUP BY c.state
ORDER BY total_revenue DESC;

-- 7. Customer Lifetime Value
SELECT
    c.customer_id,
    c.full_name,
    SUM(f.line_total) AS lifetime_value,
    COUNT(DISTINCT f.transaction_id) AS total_transactions
FROM warehouse.fact_sales f
JOIN warehouse.dim_customers c
    ON f.customer_key = c.customer_key
GROUP BY c.customer_id, c.full_name
ORDER BY lifetime_value DESC;

-- 8. Product Profitability
SELECT
    p.product_name,
    SUM(f.profit) AS total_profit,
    SUM(f.line_total) AS revenue
FROM warehouse.fact_sales f
JOIN warehouse.dim_products p
    ON f.product_key = p.product_key
GROUP BY p.product_name
ORDER BY total_profit DESC;

-- 9. Day-of-Week Sales Pattern
SELECT
    d.day_name,
    SUM(f.line_total) AS revenue
FROM warehouse.fact_sales f
JOIN warehouse.dim_date d
    ON f.date_key = d.date_key
GROUP BY d.day_name
ORDER BY revenue DESC;

-- 10. Discount Impact Analysis
SELECT
    CASE
        WHEN f.discount_percentage = 0 THEN 'No Discount'
        WHEN f.discount_percentage <= 10 THEN '1-10%'
        WHEN f.discount_percentage <= 25 THEN '11-25%'
        ELSE 'Above 25%'
    END AS discount_range,
    SUM(f.quantity) AS units_sold,
    SUM(f.line_total) AS revenue
FROM warehouse.fact_sales f
GROUP BY discount_range;
