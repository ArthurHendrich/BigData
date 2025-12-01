"""
Implementa a etapa de Transformação (Transformation):
- Limpeza de duplicados
- Tratamento de nulos simples
- Enriquecimento de colunas (região, datas, etc.)
- Geração da camada Silver
"""

from typing import Dict
import pandas as pd

from . import config


def transform_to_silver(
    dfs_bronze: Dict[str, pd.DataFrame]
) -> Dict[str, pd.DataFrame]:
    """
    Recebe os DataFrames da camada Bronze e retorna a camada Silver.

    """
    print("=== TRANSFORMAÇÃO - CAMADA SILVER ===\n")

    df_customers = dfs_bronze["customers"].copy()
    df_orders = dfs_bronze["orders"].copy()
    df_order_items = dfs_bronze["order_items"].copy()
    df_products = dfs_bronze["products"].copy()

    customers_duplicates = df_customers.duplicated().sum()
    if customers_duplicates > 0:
        df_customers = df_customers.drop_duplicates()
        print(f"Removed {customers_duplicates} duplicate rows from customers")

    if "customer_state" in df_customers.columns:
        df_customers["customer_state"] = df_customers["customer_state"].str.upper().str.strip()
        brazil_regions = {
            "AC": "North",
            "AP": "North",
            "AM": "North",
            "PA": "North",
            "RO": "North",
            "RR": "North",
            "TO": "North",
            "AL": "Northeast",
            "BA": "Northeast",
            "CE": "Northeast",
            "MA": "Northeast",
            "PB": "Northeast",
            "PE": "Northeast",
            "PI": "Northeast",
            "RN": "Northeast",
            "SE": "Northeast",
            "DF": "Center-West",
            "GO": "Center-West",
            "MT": "Center-West",
            "MS": "Center-West",
            "ES": "Southeast",
            "MG": "Southeast",
            "RJ": "Southeast",
            "SP": "Southeast",
            "PR": "South",
            "RS": "South",
            "SC": "South",
        }
        df_customers["customer_region"] = df_customers["customer_state"].map(brazil_regions)

    products_duplicates = df_products.duplicated().sum()
    if products_duplicates > 0:
        df_products = df_products.drop_duplicates()
        print(f"Removed {products_duplicates} duplicate rows from products")

    if "product_category_name" in df_products.columns:
        missing_cat = df_products["product_category_name"].isnull().sum()
        if missing_cat > 0:
            df_products["product_category_name"].fillna("undefined_category", inplace=True)
            print(f"Filled {missing_cat} missing product_category_name with 'undefined_category'")

        df_products["product_category_name"] = (
            df_products["product_category_name"].str.lower().str.strip()
        )

    orders_duplicates = df_orders.duplicated().sum()
    if orders_duplicates > 0:
        df_orders = df_orders.drop_duplicates()
        print(f"Removed {orders_duplicates} duplicate rows from orders")

    if "order_purchase_timestamp" in df_orders.columns:
        df_orders["order_purchase_timestamp"] = pd.to_datetime(
            df_orders["order_purchase_timestamp"]
        )
        df_orders["order_purchase_date"] = df_orders["order_purchase_timestamp"].dt.date
        df_orders["order_purchase_hour"] = df_orders["order_purchase_timestamp"].dt.hour

    order_items_duplicates = df_order_items.duplicated().sum()
    if order_items_duplicates > 0:
        df_order_items = df_order_items.drop_duplicates()
        print(f"Removed {order_items_duplicates} duplicate rows from order_items")


    df_customers.to_csv(config.SILVER_DIR / "customers_silver.csv", index=False)
    df_products.to_csv(config.SILVER_DIR / "products_silver.csv", index=False)
    df_orders.to_csv(config.SILVER_DIR / "orders_silver.csv", index=False)
    df_order_items.to_csv(config.SILVER_DIR / "order_items_silver.csv", index=False)

    try:
        df_customers.to_parquet(config.SILVER_DIR / "customers_silver.parquet", index=False)
        df_products.to_parquet(config.SILVER_DIR / "products_silver.parquet", index=False)
        df_orders.to_parquet(config.SILVER_DIR / "orders_silver.parquet", index=False)
        df_order_items.to_parquet(config.SILVER_DIR / "order_items_silver.parquet", index=False)
        print("\nSilver layer saved as CSV and Parquet.")
    except Exception as e:
        print("\n[WARNING] Failed to save Silver as Parquet (pyarrow not installed?).")
        print(e)

    print("\nShapes Silver:")
    print(f"  Customers   : {df_customers.shape}")
    print(f"  Orders      : {df_orders.shape}")
    print(f"  Order Items : {df_order_items.shape}")
    print(f"  Products    : {df_products.shape}")

    return {
        "customers": df_customers,
        "orders": df_orders,
        "order_items": df_order_items,
        "products": df_products,
    }
