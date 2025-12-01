from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = BASE_DIR / "dados"

BRONZE_DIR = DATA_DIR / "bronze"
SILVER_DIR = DATA_DIR / "silver"
GOLD_DIR = DATA_DIR / "gold"

for d in [DATA_DIR, BRONZE_DIR, SILVER_DIR, GOLD_DIR]:
    d.mkdir(parents=True, exist_ok=True)

CUSTOMERS_FILE = "olist_customers_dataset.csv"
ORDERS_FILE = "olist_orders_dataset.csv"
ORDER_ITEMS_FILE = "olist_order_items_dataset.csv"
PRODUCTS_FILE = "olist_products_dataset.csv"
