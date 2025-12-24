-- =========================================
-- DATA QUALITY CHECKS - STAGING
-- =========================================

-- 1. NULL CHECKS
SELECT 'customers.email' AS field, COUNT(*) AS null_count
FROM staging.customers
WHERE email IS NULL;

SELECT 'products.price' AS field, COUNT(*) AS null_count
FROM staging.products
WHERE price IS NULL;

-- 2. DUPLICATE CHECKS
SELECT customer_id, COUNT(*)
FROM staging.customers
GROUP BY customer_id
HAVING COUNT(*) > 1;

-- 3. REFERENTIAL INTEGRITY
-- Orphan transactions
SELECT COUNT(*) AS orphan_transactions
FROM staging.transactions t
LEFT JOIN staging.customers c
ON t.customer_id = c.customer_id
WHERE c.customer_id IS NULL;

-- Orphan transaction items (transaction)
SELECT COUNT(*) AS orphan_items_transactions
FROM staging.transaction_items ti
LEFT JOIN staging.transactions t
ON ti.transaction_id = t.transaction_id
WHERE t.transaction_id IS NULL;

-- Orphan transaction items (product)
SELECT COUNT(*) AS orphan_items_products
FROM staging.transaction_items ti
LEFT JOIN staging.products p
ON ti.product_id = p.product_id
WHERE p.product_id IS NULL;

-- 4. RANGE CHECKS
SELECT COUNT(*) AS invalid_prices
FROM staging.products
WHERE price <= 0;

SELECT COUNT(*) AS invalid_discounts
FROM staging.transaction_items
WHERE discount_percentage < 0 OR discount_percentage > 100;

-- 5. CONSISTENCY CHECK
SELECT COUNT(*) AS inconsistent_line_totals
FROM staging.transaction_items
WHERE ROUND(line_total,2) != ROUND(quantity * unit_price * (1 - discount_percentage/100),2);
