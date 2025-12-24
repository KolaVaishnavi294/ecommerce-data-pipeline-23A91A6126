import psycopg2
import pandas as pd
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

RAW_DATA_PATH = "data/raw"
SUMMARY_PATH = "docs/ingestion_summary.json"


# ---------------------------------
# DATABASE CONNECTION
# ---------------------------------
def get_connection():
    return psycopg2.connect(**DB_CONFIG)


# ---------------------------------
# BULK LOAD FUNCTION
# ---------------------------------
def load_csv_to_table(conn, csv_file, table_name):
    df = pd.read_csv(csv_file)

    cols = ",".join(df.columns)
    placeholders = ",".join(["%s"] * len(df.columns))
    insert_query = f"""
        INSERT INTO {table_name} ({cols})
        VALUES ({placeholders})
    """

    with conn.cursor() as cur:
        cur.executemany(insert_query, df.values.tolist())


# ---------------------------------
# MAIN INGESTION LOGIC
# ---------------------------------
def main():
    start_time = datetime.utcnow()
    summary = {
        "start_time": start_time.isoformat(),
        "tables_loaded": {},
        "status": "SUCCESS"
    }

    conn = get_connection()
    conn.autocommit = False  # IMPORTANT

    try:
        load_csv_to_table(
            conn,
            f"{RAW_DATA_PATH}/customers.csv",
            "staging.customers"
        )
        summary["tables_loaded"]["staging.customers"] = "customers.csv"

        load_csv_to_table(
            conn,
            f"{RAW_DATA_PATH}/products.csv",
            "staging.products"
        )
        summary["tables_loaded"]["staging.products"] = "products.csv"

        load_csv_to_table(
            conn,
            f"{RAW_DATA_PATH}/transactions.csv",
            "staging.transactions"
        )
        summary["tables_loaded"]["staging.transactions"] = "transactions.csv"

        load_csv_to_table(
            conn,
            f"{RAW_DATA_PATH}/transaction_items.csv",
            "staging.transaction_items"
        )
        summary["tables_loaded"]["staging.transaction_items"] = "transaction_items.csv"

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

        print("📥 Data ingestion completed")
        print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
