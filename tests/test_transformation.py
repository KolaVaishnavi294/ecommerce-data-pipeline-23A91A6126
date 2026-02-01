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


def test_production_tables_populated():
    conn = get_connection()
    cur = conn.cursor()

    tables = [
        "production.customers",
        "production.products",
        "production.transactions",
        "production.transaction_items",
    ]

    for table in tables:
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        assert cur.fetchone()[0] > 0

    conn.close()


def test_email_lowercase():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*) FROM production.customers
        WHERE email != LOWER(email)
    """)
    assert cur.fetchone()[0] == 0

    conn.close()
