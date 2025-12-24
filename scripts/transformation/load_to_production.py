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

SUMMARY_PATH = "docs/transformation_summary.json"


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
            # LOAD CUSTOMERS
            # ---------------------------------
            cur.execute("TRUNCATE TABLE production.customers CASCADE")

            cur.execute("""
                INSERT INTO production.customers (
                    customer_id, first_name, last_name, email,
                    phone, registration_date, city, state, country,
                    age_group
                )
                SELECT
                    customer_id,
                    INITCAP(first_name),
                    INITCAP(last_name),
                    LOWER(email),
                    phone,
                    registration_date,
                    city,
                    state,
                    country,
                    age_group
                FROM staging.customers
            """)
            summary["tables_loaded"]["production.customers"] = "SUCCESS"

            # ---------------------------------
            # LOAD PRODUCTS
            # ---------------------------------
            cur.execute("TRUNCATE TABLE production.products CASCADE")

            cur.execute("""
                INSERT INTO production.products (
                    product_id, product_name, category, sub_category,
                    price, cost, brand, stock_quantity, supplier_id
                )
                SELECT
                    product_id,
                    INITCAP(product_name),
                    category,
                    sub_category,
                    price,
                    cost,
                    brand,
                    stock_quantity,
                    supplier_id
                FROM staging.products
            """)
            summary["tables_loaded"]["production.products"] = "SUCCESS"

            # ---------------------------------
            # LOAD TRANSACTIONS
            # ---------------------------------
            cur.execute("TRUNCATE TABLE production.transactions CASCADE")

            cur.execute("""
                INSERT INTO production.transactions (
                    transaction_id, customer_id, transaction_date,
                    transaction_time, payment_method, shipping_address,
                    total_amount
                )
                SELECT
                    transaction_id,
                    customer_id,
                    transaction_date,
                    transaction_time,
                    payment_method,
                    shipping_address,
                    total_amount
                FROM staging.transactions
            """)
            summary["tables_loaded"]["production.transactions"] = "SUCCESS"

            # ---------------------------------
            # LOAD TRANSACTION ITEMS
            # ---------------------------------
            cur.execute("TRUNCATE TABLE production.transaction_items CASCADE")

            cur.execute("""
                INSERT INTO production.transaction_items (
                    item_id, transaction_id, product_id,
                    quantity, unit_price, discount_percentage, line_total
                )
                SELECT
                    item_id,
                    transaction_id,
                    product_id,
                    quantity,
                    unit_price,
                    discount_percentage,
                    line_total
                FROM staging.transaction_items
            """)
            summary["tables_loaded"]["production.transaction_items"] = "SUCCESS"

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

        print("🚀 Staging to production ETL completed")
        print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
