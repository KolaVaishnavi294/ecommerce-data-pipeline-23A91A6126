import pandas as pd
import random
import json
import os
from faker import Faker
from datetime import datetime, date
import yaml

# ---------------------------------
# INITIAL SETUP
# ---------------------------------
fake = Faker()

RAW_DATA_PATH = "data/raw"
os.makedirs(RAW_DATA_PATH, exist_ok=True)


# ---------------------------------
# LOAD CONFIG
# ---------------------------------
def load_config():
    with open("config/config.yaml", "r") as f:
        return yaml.safe_load(f)


config = load_config()

# Convert date strings from YAML to date objects (IMPORTANT for Faker)
START_DATE = datetime.strptime(
    config["data_generation"]["start_date"], "%Y-%m-%d"
).date()

END_DATE = datetime.strptime(
    config["data_generation"]["end_date"], "%Y-%m-%d"
).date()


# ---------------------------------
# REQUIRED FUNCTIONS (MANDATORY)
# ---------------------------------

def generate_customers(num_customers: int) -> pd.DataFrame:
    customers = []

    for i in range(1, num_customers + 1):
        customers.append({
            "customer_id": f"CUST{i:04d}",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": f"user{i}@example.com",  # unique emails
            "phone": fake.msisdn()[:10],
            "registration_date": fake.date_between(
                start_date=START_DATE,
                end_date=END_DATE
            ),
            "city": fake.city(),
            "state": fake.state(),
            "country": "India",
            "age_group": random.choice(["18-25", "26-35", "36-45", "46-60"])
        })

    return pd.DataFrame(customers)


def generate_products(num_products: int) -> pd.DataFrame:
    categories = {
        "Electronics": (100, 1000),
        "Clothing": (20, 200),
        "Home & Kitchen": (50, 500),
        "Books": (10, 100),
        "Sports": (30, 300),
        "Beauty": (15, 150)
    }

    products = []

    for i in range(1, num_products + 1):
        category = random.choice(list(categories.keys()))
        min_price, max_price = categories[category]

        price = round(random.uniform(min_price, max_price), 2)
        cost = round(price * random.uniform(0.6, 0.85), 2)  # cost < price

        products.append({
            "product_id": f"PROD{i:04d}",
            "product_name": fake.word().capitalize(),
            "category": category,
            "sub_category": fake.word().capitalize(),
            "price": price,
            "cost": cost,
            "brand": fake.company(),
            "stock_quantity": random.randint(10, 500),
            "supplier_id": f"SUP{random.randint(1, 50):03d}"
        })

    return pd.DataFrame(products)


def generate_transactions(
    num_transactions: int,
    customers_df: pd.DataFrame
) -> pd.DataFrame:

    payment_methods = [
        "Credit Card", "Debit Card", "UPI",
        "Cash on Delivery", "Net Banking"
    ]

    transactions = []

    for i in range(1, num_transactions + 1):
        transactions.append({
            "transaction_id": f"TXN{i:05d}",
            "customer_id": random.choice(customers_df["customer_id"]),
            "transaction_date": fake.date_between(
                start_date=START_DATE,
                end_date=END_DATE
            ),
            "transaction_time": fake.time(),
            "payment_method": random.choice(payment_methods),
            "shipping_address": fake.address().replace("\n", ", "),
            "total_amount": 0.0  # calculated later
        })

    return pd.DataFrame(transactions)


def generate_transaction_items(
    transactions_df: pd.DataFrame,
    products_df: pd.DataFrame
) -> pd.DataFrame:

    items = []
    item_counter = 1

    for _, txn in transactions_df.iterrows():
        num_items = random.randint(1, 5)
        selected_products = products_df.sample(num_items)

        transaction_total = 0.0

        for _, prod in selected_products.iterrows():
            quantity = random.randint(1, 4)
            discount = random.choice([0, 5, 10, 15, 20])

            line_total = round(
                quantity * prod["price"] * (1 - discount / 100),
                2
            )

            transaction_total += line_total

            items.append({
                "item_id": f"ITEM{item_counter:05d}",
                "transaction_id": txn["transaction_id"],
                "product_id": prod["product_id"],
                "quantity": quantity,
                "unit_price": prod["price"],
                "discount_percentage": discount,
                "line_total": line_total
            })

            item_counter += 1

        transactions_df.loc[
            transactions_df["transaction_id"] == txn["transaction_id"],
            "total_amount"
        ] = round(transaction_total, 2)

    return pd.DataFrame(items)


def validate_referential_integrity(
    customers: pd.DataFrame,
    products: pd.DataFrame,
    transactions: pd.DataFrame,
    items: pd.DataFrame
) -> dict:

    orphan_transactions = ~transactions["customer_id"].isin(
        customers["customer_id"]
    )

    orphan_items_txn = ~items["transaction_id"].isin(
        transactions["transaction_id"]
    )

    orphan_items_prod = ~items["product_id"].isin(
        products["product_id"]
    )

    return {
        "orphan_transactions": int(orphan_transactions.sum()),
        "orphan_items_transactions": int(orphan_items_txn.sum()),
        "orphan_items_products": int(orphan_items_prod.sum()),
        "status": "PASS"
        if orphan_transactions.sum() == 0
        and orphan_items_txn.sum() == 0
        and orphan_items_prod.sum() == 0
        else "FAIL"
    }


# ---------------------------------
# MAIN EXECUTION
# ---------------------------------
if __name__ == "__main__":

    customers_df = generate_customers(
        config["data_generation"]["customers"]
    )

    products_df = generate_products(
        config["data_generation"]["products"]
    )

    transactions_df = generate_transactions(
        config["data_generation"]["transactions"],
        customers_df
    )

    items_df = generate_transaction_items(
        transactions_df,
        products_df
    )

    integrity_report = validate_referential_integrity(
        customers_df,
        products_df,
        transactions_df,
        items_df
    )

    # Save CSV files
    customers_df.to_csv(
        f"{RAW_DATA_PATH}/customers.csv", index=False
    )
    products_df.to_csv(
        f"{RAW_DATA_PATH}/products.csv", index=False
    )
    transactions_df.to_csv(
        f"{RAW_DATA_PATH}/transactions.csv", index=False
    )
    items_df.to_csv(
        f"{RAW_DATA_PATH}/transaction_items.csv", index=False
    )

    # Save metadata JSON
    metadata = {
        "generation_timestamp": datetime.utcnow().isoformat(),
        "records": {
            "customers": len(customers_df),
            "products": len(products_df),
            "transactions": len(transactions_df),
            "transaction_items": len(items_df)
        },
        "referential_integrity": integrity_report
    }

    with open(
        f"{RAW_DATA_PATH}/generation_metadata.json", "w"
    ) as f:
        json.dump(metadata, f, indent=4)

    print("Data generation completed successfully")
    print(json.dumps(metadata, indent=2))
