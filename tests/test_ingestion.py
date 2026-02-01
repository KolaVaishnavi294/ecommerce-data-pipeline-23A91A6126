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


def test_staging_tables_exist():
    conn = get_connection()
    cur = conn.cursor()

    tables = [
        "staging.customers",
        "staging.products",
        "staging.transactions",
        "staging.transaction_items",
    ]

    for table in tables:
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        count = cur.fetchone()[0]
        assert count > 0

    conn.close()
