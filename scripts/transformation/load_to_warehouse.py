import psycopg2
import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}

SUMMARY_PATH = "docs/warehouse_load_summary.json"


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def main():
    conn = get_connection()
    conn.autocommit = False

    summary = {
        "start_time": datetime.utcnow().isoformat(),
        "tables_loaded": {},
        "status": "SUCCESS"
    }

    try:
        with conn.cursor() as cur:

            # ---------------------------------
            # DIM DATE
            # ---------------------------------
            cur.execute("TRUNCATE TABLE warehouse.dim_date CASCADE")
            cur.execute("""
                INSERT INTO warehouse.dim_date (
                    date_key, full_date, year, quarter, month, day,
                    month_name, day_name, week_of_year, is_weekend
                )
                SELECT DISTINCT
                    TO_CHAR(transaction_date, 'YYYYMMDD')::INTEGER AS date_key,
                    transaction_date,
                    EXTRACT(YEAR FROM transaction_date),
                    EXTRACT(QUARTER FROM transaction_date),
                    EXTRACT(MONTH FROM transaction_date),
                    EXTRACT(DAY FROM transaction_date),
                    TO_CHAR(transaction_date, 'Month'),
                    TO_CHAR(transaction_date, 'Day'),
                    EXTRACT(WEEK FROM transaction_date),
                    CASE WHEN EXTRACT(DOW FROM transaction_date) IN (0,6)
                         THEN TRUE ELSE FALSE END
                FROM production.transactions
            """)
            summary["warehouse.dim_date"] = "SUCCESS"

            # ---------------------------------
            # DIM PAYMENT METHOD
            # ---------------------------------
            cur.execute("TRUNCATE TABLE warehouse.dim_payment_method CASCADE")
            cur.execute("""
                INSERT INTO warehouse.dim_payment_method (
                    payment_method_name, payment_type
                )
                SELECT DISTINCT
                    payment_method,
                    CASE
                        WHEN payment_method IN ('UPI', 'Net Banking')
                            THEN 'Online'
                        ELSE 'Card/COD'
                    END
                FROM production.transactions
            """)
            summary["warehouse.dim_payment_method"] = "SUCCESS"

            # ---------------------------------
            # DIM CUSTOMERS (SCD READY)
            # ---------------------------------
            cur.execute("TRUNCATE TABLE warehouse.dim_customers CASCADE")
            cur.execute("""
                INSERT INTO warehouse.dim_customers (
                    customer_id, full_name, email, city, state,
                    country, age_group, customer_segment,
                    registration_date, effective_date, is_current
                )
                SELECT
                    customer_id,
                    first_name || ' ' || last_name,
                    email,
                    city,
                    state,
                    country,
                    age_group,
                    CASE
                        WHEN age_group IN ('18-25','26-35') THEN 'Young'
                        WHEN age_group IN ('36-45') THEN 'Mid-age'
                        ELSE 'Senior'
                    END,
                    registration_date,
                    CURRENT_DATE,
                    TRUE
                FROM production.customers
            """)
            summary["warehouse.dim_customers"] = "SUCCESS"

            # ---------------------------------
            # DIM PRODUCTS (SCD READY)
            # ---------------------------------
            cur.execute("TRUNCATE TABLE warehouse.dim_products CASCADE")
            cur.execute("""
                INSERT INTO warehouse.dim_products (
                    product_id, product_name, category,
                    sub_category, brand, price_range,
                    effective_date, is_current
                )
                SELECT
                    product_id,
                    product_name,
                    category,
                    sub_category,
                    brand,
                    CASE
                        WHEN price < 100 THEN 'Budget'
                        WHEN price BETWEEN 100 AND 500 THEN 'Mid-range'
                        ELSE 'Premium'
                    END,
                    CURRENT_DATE,
                    TRUE
                FROM production.products
            """)
            summary["warehouse.dim_products"] = "SUCCESS"

            # ---------------------------------
            # FACT SALES (LINE ITEM GRAIN)
            # ---------------------------------
            cur.execute("TRUNCATE TABLE warehouse.fact_sales CASCADE")
            cur.execute("""
                INSERT INTO warehouse.fact_sales (
                    date_key, customer_key, product_key,
                    payment_method_key, transaction_id,
                    quantity, unit_price, discount_amount,
                    line_total, profit
                )
                SELECT
                    TO_CHAR(t.transaction_date, 'YYYYMMDD')::INTEGER,
                    dc.customer_key,
                    dp.product_key,
                    dpm.payment_method_key,
                    ti.transaction_id,
                    ti.quantity,
                    ti.unit_price,
                    (ti.unit_price * ti.quantity) - ti.line_total,
                    ti.line_total,
                    ti.line_total - (ti.quantity * p.cost)
                FROM production.transaction_items ti
                JOIN production.transactions t
                    ON ti.transaction_id = t.transaction_id
                JOIN production.products p
                    ON ti.product_id = p.product_id
                JOIN warehouse.dim_customers dc
                    ON dc.customer_id = t.customer_id AND dc.is_current = TRUE
                JOIN warehouse.dim_products dp
                    ON dp.product_id = ti.product_id AND dp.is_current = TRUE
                JOIN warehouse.dim_payment_method dpm
                    ON dpm.payment_method_name = t.payment_method
            """)
            summary["warehouse.fact_sales"] = "SUCCESS"

        conn.commit()

    except Exception as e:
        conn.rollback()
        summary["status"] = "FAILED"
        summary["error"] = str(e)

    finally:
        conn.close()
        summary["end_time"] = datetime.utcnow().isoformat()

        with open(SUMMARY_PATH, "w") as f:
            json.dump(summary, f, indent=4)

        print("Warehouse ETL completed")
        print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
