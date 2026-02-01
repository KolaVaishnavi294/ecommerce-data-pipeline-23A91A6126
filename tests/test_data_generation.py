import pandas as pd
import numpy as np
from pathlib import Path
import pytest

DATA_RAW = Path("data/raw")


def test_raw_files_exist():
    assert (DATA_RAW / "customers.csv").exists()
    assert (DATA_RAW / "products.csv").exists()
    assert (DATA_RAW / "transactions.csv").exists()
    assert (DATA_RAW / "transaction_items.csv").exists()


def test_customer_count():
    df = pd.read_csv(DATA_RAW / "customers.csv")
    assert len(df) == 1000


def test_product_count():
    df = pd.read_csv(DATA_RAW / "products.csv")
    assert len(df) == 500


def test_transaction_integrity():
    customers = pd.read_csv(DATA_RAW / "customers.csv")
    transactions = pd.read_csv(DATA_RAW / "transactions.csv")

    assert transactions["customer_id"].isin(customers["customer_id"]).all()


def test_line_total_calculation():
    items = pd.read_csv(DATA_RAW / "transaction_items.csv")

    recalculated = (
        items["quantity"]
        * items["unit_price"]
        * (1 - items["discount_percentage"] / 100)
    )

    # Floating point safe comparison
    assert np.allclose(
        recalculated,
        items["line_total"],
        atol=0.01
    )
