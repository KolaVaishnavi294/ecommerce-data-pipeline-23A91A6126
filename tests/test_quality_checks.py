import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )


def test_no_orphan_transactions():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*)
        FROM production.transactions t
        LEFT JOIN production.customers c
        ON t.customer_id = c.customer_id
        WHERE c.customer_id IS NULL
    """)

    assert cur.fetchone()[0] == 0
    conn.close()


def test_no_orphan_transaction_items_transactions():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*)
        FROM production.transaction_items ti
        LEFT JOIN production.transactions t
        ON ti.transaction_id = t.transaction_id
        WHERE t.transaction_id IS NULL
    """)

    assert cur.fetchone()[0] == 0
    conn.close()


def test_no_orphan_transaction_items_products():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*)
        FROM production.transaction_items ti
        LEFT JOIN production.products p
        ON ti.product_id = p.product_id
        WHERE p.product_id IS NULL
    """)

    assert cur.fetchone()[0] == 0
    conn.close()


def test_discount_range_valid():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*)
        FROM production.transaction_items
        WHERE discount_percentage < 0 OR discount_percentage > 100
    """)

    assert cur.fetchone()[0] == 0
    conn.close()
