"""
Geração de visualizações e dashboards a partir da camada Silver/Gold.

As figuras são salvas em:
    dados/gold/figures/*.png

Essas imagens podem ser usadas:
- na apresentação de slides
- no README / relatório
- em notebooks de exploração
"""

from pathlib import Path
from typing import Dict

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from . import config


def generate_all_visualizations(
    dfs_silver: Dict[str, pd.DataFrame],
    products_by_category: pd.DataFrame,
    customers_by_region: pd.DataFrame,
    product_reco_stats: pd.DataFrame,
) -> Dict[str, Path]:
    """
    Gera e salva os principais gráficos do projeto.

    Retorna um dicionário {nome_do_grafico: caminho_png}.
    """
    output_dir = config.GOLD_DIR / "figures"
    output_dir.mkdir(parents=True, exist_ok=True)

    sns.set_style("whitegrid")

    df_customers = dfs_silver["customers"]
    df_orders = dfs_silver["orders"]
    df_order_items = dfs_silver["order_items"]
    df_products = dfs_silver["products"]

    figure_paths: Dict[str, Path] = {}

    if not products_by_category.empty:
        plt.figure(figsize=(10, 6))
        top10 = products_by_category.head(10).iloc[::-1]
        plt.barh(top10.index, top10["product_count"])
        plt.title("Top 10 categorias de produto (catálogo)")
        plt.xlabel("Quantidade de produtos")
        plt.tight_layout()
        path = output_dir / "top10_product_categories.png"
        plt.savefig(path)
        plt.close()
        figure_paths["top10_product_categories"] = path

        if "customer_region" in df_customers.columns:
            customers_by_region = (
                df_customers
                .groupby("customer_region")
                .size()
                .reset_index(name="count")
                .sort_values("count", ascending=False)
            )
        else:
            customers_by_region = pd.DataFrame(columns=["customer_region", "count"])

        if not customers_by_region.empty:
            plt.figure(figsize=(8, 5))
            plt.bar(customers_by_region["customer_region"], customers_by_region["count"])
            plt.title("Distribuição de clientes por região")
            plt.ylabel("Número de clientes")
            plt.xticks(rotation=30)
            plt.tight_layout()
            path = output_dir / "customers_by_region.png"
            plt.savefig(path)
            plt.close()
            figure_paths["customers_by_region"] = path
        else:
            print("Nenhuma informação de região de cliente disponível; gráfico 'customers_by_region' não gerado.")


    if not product_reco_stats.empty:
        plt.figure(figsize=(10, 6))
        top10_reco = (
            product_reco_stats.sort_values("total_orders", ascending=False)
            .head(10)
            .iloc[::-1]
        )
        plt.barh(top10_reco["product_id"], top10_reco["total_orders"])
        plt.title("Top 10 produtos mais vendidos (por número de pedidos)")
        plt.xlabel("Total de pedidos (delivered)")
        plt.tight_layout()
        path = output_dir / "top10_products_by_orders.png"
        plt.savefig(path)
        plt.close()
        figure_paths["top10_products_by_orders"] = path

    if "order_purchase_timestamp" in df_orders.columns:
        df_orders_copy = df_orders.copy()
        df_orders_copy["order_purchase_timestamp"] = pd.to_datetime(
            df_orders_copy["order_purchase_timestamp"]
        )
        df_orders_copy["year"] = df_orders_copy["order_purchase_timestamp"].dt.year
        orders_by_year = df_orders_copy["year"].value_counts().sort_index()

        plt.figure(figsize=(8, 5))
        plt.plot(orders_by_year.index, orders_by_year.values, marker="o")
        plt.title("Número de pedidos por ano")
        plt.xlabel("Ano")
        plt.ylabel("Quantidade de pedidos")
        plt.tight_layout()
        path = output_dir / "orders_by_year.png"
        plt.savefig(path)
        plt.close()
        figure_paths["orders_by_year"] = path

    numeric_cols = [
        c
        for c in ["product_weight_g", "product_length_cm", "product_height_cm", "product_width_cm"]
        if c in df_products.columns
    ]
    if numeric_cols:
        plt.figure(figsize=(8, 6))
        sns.heatmap(df_products[numeric_cols].corr(), annot=True, fmt=".2f")
        plt.title("Correlação entre atributos físicos dos produtos")
        plt.tight_layout()
        path = output_dir / "products_numeric_corr.png"
        plt.savefig(path)
        plt.close()
        figure_paths["products_numeric_corr"] = path

    print("\nVisualizações salvas em:", output_dir)
    for name, path in figure_paths.items():
        print(f"  - {name}: {path}")

    return figure_paths
