"""
Implementa a etapa de Ingestão (Ingestion) do pipeline, em modo batch:
- Lê arquivos CSV do diretório de dados "dados/"
- Salva cópias na camada Bronze (BRONZE_DIR)
"""

from pathlib import Path
from typing import Dict

import pandas as pd

from . import config, data_sources


def _read_csv_if_exists(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")
    df = pd.read_csv(path)
    return df


def ingest_bronze() -> Dict[str, pd.DataFrame]:
    print("=== INGESTÃO (BATCH) - CAMADA BRONZE ===\n")

    data_sources.describe_sources()

    customers_path = config.DATA_DIR / config.CUSTOMERS_FILE
    orders_path = config.DATA_DIR / config.ORDERS_FILE
    order_items_path = config.DATA_DIR / config.ORDER_ITEMS_FILE
    products_path = config.DATA_DIR / config.PRODUCTS_FILE

    df_customers = _read_csv_if_exists(customers_path)
    df_orders = _read_csv_if_exists(orders_path)
    df_order_items = _read_csv_if_exists(order_items_path)
    df_products = _read_csv_if_exists(products_path)

    print("Shapes pós-ingestão (dados brutos):")
    print(f"  Customers   : {df_customers.shape}")
    print(f"  Orders      : {df_orders.shape}")
    print(f"  Order Items : {df_order_items.shape}")
    print(f"  Products    : {df_products.shape}")

    df_customers.to_csv(config.BRONZE_DIR / config.CUSTOMERS_FILE, index=False)
    df_orders.to_csv(config.BRONZE_DIR / config.ORDERS_FILE, index=False)
    df_order_items.to_csv(config.BRONZE_DIR / config.ORDER_ITEMS_FILE, index=False)
    df_products.to_csv(config.BRONZE_DIR / config.PRODUCTS_FILE, index=False)

    print("\nArquivos Bronze salvos em:", config.BRONZE_DIR)

    return {
        "customers": df_customers,
        "orders": df_orders,
        "order_items": df_order_items,
        "products": df_products,
    }
