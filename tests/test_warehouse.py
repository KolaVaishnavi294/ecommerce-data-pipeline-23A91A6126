import psycopg2
import os
from dotenv import load_dotenv
import pytest

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )


def test_warehouse_counts():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM warehouse.dim_customers")
    assert cur.fetchone()[0] == 1000

    cur.execute("SELECT COUNT(*) FROM warehouse.dim_products")
    assert cur.fetchone()[0] == 500

    cur.execute("SELECT COUNT(*) FROM warehouse.fact_sales")
    assert cur.fetchone()[0] > 0

    conn.close()


def test_fact_sales_grain():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*) 
        FROM warehouse.fact_sales
        WHERE quantity <= 0 OR line_total <= 0
    """)
    assert cur.fetchone()[0] == 0

    conn.close()
