"""
Implementa a camada Gold (Destination) com:
- Métricas de negócio (categorias, regiões etc.)
- Métricas voltadas para recomendação de produtos:
  - popularidade por produto
  - histórico cliente x categoria
"""

from typing import Dict, Tuple
import pandas as pd

from . import config


def build_gold_tables(
    dfs_silver: Dict[str, pd.DataFrame]
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Recebe os DataFrames Silver e gera:
      - products_by_category (negócio)
      - customers_by_region (negócio)
      - product_recommendation_stats (recomendação)
      - customer_category_history (recomendação)

    Também salva os CSVs na camada Gold.
    """
    print("=== GOLD LAYER - BUSINESS & RECOMMENDATION METRICS ===\n")

    df_customers = dfs_silver["customers"]
    df_orders = dfs_silver["orders"]
    df_order_items = dfs_silver["order_items"]
    df_products = dfs_silver["products"]


    if "product_category_name" in df_products.columns:
        products_by_category = (
            df_products.groupby("product_category_name")
            .agg(product_count=("product_id", "count"))
            .sort_values("product_count", ascending=False)
        )
    else:
        products_by_category = pd.DataFrame()

    if "customer_region" in df_customers.columns:
        customers_by_region = (
            df_customers["customer_region"]
            .value_counts()
            .reset_index()
            .rename(columns={"index": "customer_region", "customer_region": "count"})
        )
    else:
        customers_by_region = pd.DataFrame()

    required_orders_cols = {
        "order_id",
        "customer_id",
        "order_status",
        "order_purchase_timestamp",
    }
    required_items_cols = {"order_id", "order_item_id", "product_id", "price"}

    if required_orders_cols.issubset(df_orders.columns) and required_items_cols.issubset(
        df_order_items.columns
    ):
        fact_orders = (
            df_order_items[["order_id", "order_item_id", "product_id", "price"]]
            .merge(
                df_orders[list(required_orders_cols)],
                on="order_id",
                how="left",
            )
            .merge(
                df_customers[
                    ["customer_id", "customer_unique_id", "customer_state", "customer_region"]
                ],
                on="customer_id",
                how="left",
            )
            .merge(
                df_products[["product_id", "product_category_name"]],
                on="product_id",
                how="left",
            )
        )

        fact_delivered = fact_orders[
            fact_orders["order_status"] == "delivered"
        ].copy()

        product_recommendation_stats = (
            fact_delivered.groupby(["product_id", "product_category_name"])
            .agg(
                total_orders=("order_id", "nunique"),
                total_quantity=("order_item_id", "count"),
                unique_customers=("customer_unique_id", "nunique"),
                total_revenue=("price", "sum"),
                avg_price=("price", "mean"),
            )
            .reset_index()
            .sort_values("total_orders", ascending=False)
        )

        customer_category_history = (
            fact_delivered.groupby(["customer_unique_id", "product_category_name"])
            .agg(
                orders=("order_id", "nunique"),
                total_quantity=("order_item_id", "count"),
            )
            .reset_index()
        )
    else:
        print(
            "[WARNING] Orders / order_items não possuem as colunas esperadas. "
            "Tabelas de recomendação não foram geradas."
        )
        product_recommendation_stats = pd.DataFrame()
        customer_category_history = pd.DataFrame()


    products_by_category.to_csv(config.GOLD_DIR / "gold_category_analysis.csv")
    customers_by_region.to_csv(config.GOLD_DIR / "gold_customers_by_region.csv", index=False)
    product_recommendation_stats.to_csv(
        config.GOLD_DIR / "gold_product_recommendation_stats.csv", index=False
    )
    customer_category_history.to_csv(
        config.GOLD_DIR / "gold_customer_category_history.csv", index=False
    )

    if not products_by_category.empty:
        top_category = products_by_category.index[0]
    else:
        top_category = "N/A"

    if not customers_by_region.empty:
        if "customer_region" in customers_by_region.columns:
            top_region = customers_by_region["customer_region"].iloc[0]
        else:
            top_region = customers_by_region.iloc[0, 0]
    else:
        top_region = "N/A"

    top_insights = pd.DataFrame(
        {
            "Insight": [
                "Top product category by count",
                "Top customer region by count",
                "Total products",
                "Total customers",
            ],
            "Value": [
                top_category,
                top_region,
                len(df_products),
                len(df_customers),
            ],
        }
    )
    top_insights.to_csv(config.GOLD_DIR / "gold_top_insights.csv", index=False)

    print("Arquivos Gold gerados em:", config.GOLD_DIR)

    return products_by_category, customers_by_region, product_recommendation_stats
