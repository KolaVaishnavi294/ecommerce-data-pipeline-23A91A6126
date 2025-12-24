import psycopg2
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# ---------------------------------
# LOAD ENVIRONMENT VARIABLES
# ---------------------------------
load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}

REPORT_PATH = "docs/quality/quality_report.json"


# ---------------------------------
# DATABASE CONNECTION
# ---------------------------------
def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def run_scalar_query(conn, query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchone()[0]


# ---------------------------------
# MAIN QUALITY CHECK LOGIC
# ---------------------------------
def main():
    conn = get_connection()

    report = {
        "check_timestamp": datetime.utcnow().isoformat(),
        "checks": {},
        "overall_quality_score": 0
    }

    try:
        # -----------------------------
        # COMPLETENESS CHECKS
        # -----------------------------
        null_email = run_scalar_query(
            conn,
            "SELECT COUNT(*) FROM staging.customers WHERE email IS NULL"
        )

        report["checks"]["null_checks"] = {
            "customers.email": null_email
        }

        # -----------------------------
        # DUPLICATE CHECKS
        # -----------------------------
        duplicate_customers = run_scalar_query(
            conn,
            """
            SELECT COUNT(*) FROM (
                SELECT customer_id
                FROM staging.customers
                GROUP BY customer_id
                HAVING COUNT(*) > 1
            ) sub
            """
        )

        report["checks"]["duplicate_checks"] = {
            "duplicate_customers": duplicate_customers
        }

        # -----------------------------
        # REFERENTIAL INTEGRITY CHECKS
        # -----------------------------
        orphan_transactions = run_scalar_query(
            conn,
            """
            SELECT COUNT(*)
            FROM staging.transactions t
            LEFT JOIN staging.customers c
            ON t.customer_id = c.customer_id
            WHERE c.customer_id IS NULL
            """
        )

        orphan_items_transactions = run_scalar_query(
            conn,
            """
            SELECT COUNT(*)
            FROM staging.transaction_items ti
            LEFT JOIN staging.transactions t
            ON ti.transaction_id = t.transaction_id
            WHERE t.transaction_id IS NULL
            """
        )

        orphan_items_products = run_scalar_query(
            conn,
            """
            SELECT COUNT(*)
            FROM staging.transaction_items ti
            LEFT JOIN staging.products p
            ON ti.product_id = p.product_id
            WHERE p.product_id IS NULL
            """
        )

        report["checks"]["referential_integrity"] = {
            "orphan_transactions": orphan_transactions,
            "orphan_items_transactions": orphan_items_transactions,
            "orphan_items_products": orphan_items_products
        }

        # -----------------------------
        # RANGE CHECKS
        # -----------------------------
        invalid_prices = run_scalar_query(
            conn,
            "SELECT COUNT(*) FROM staging.products WHERE price <= 0"
        )

        invalid_discounts = run_scalar_query(
            conn,
            """
            SELECT COUNT(*)
            FROM staging.transaction_items
            WHERE discount_percentage < 0 OR discount_percentage > 100
            """
        )

        report["checks"]["range_checks"] = {
            "invalid_prices": invalid_prices,
            "invalid_discounts": invalid_discounts
        }

        # -----------------------------
        # CONSISTENCY CHECK (WITH TOLERANCE)
        # -----------------------------
        inconsistent_lines = run_scalar_query(
            conn,
            """
            SELECT COUNT(*)
            FROM staging.transaction_items
            WHERE ABS(
                line_total - (quantity * unit_price * (1 - discount_percentage / 100))
            ) > 0.01
            """
        )

        report["checks"]["consistency_checks"] = {
            "inconsistent_line_totals": inconsistent_lines
        }

        # -----------------------------
        # QUALITY SCORE CALCULATION
        # -----------------------------
        total_records = run_scalar_query(
            conn,
            "SELECT COUNT(*) FROM staging.transaction_items"
        )

        if total_records == 0:
            report["overall_quality_score"] = 100
        else:
            penalty = (inconsistent_lines / total_records) * 100
            report["overall_quality_score"] = round(100 - penalty, 2)

    finally:
        conn.close()
        os.makedirs("docs/quality", exist_ok=True)

        with open(REPORT_PATH, "w") as f:
            json.dump(report, f, indent=4)

        print("✅ Data quality checks completed")
        print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
