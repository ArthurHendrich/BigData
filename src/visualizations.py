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
        # Grafico: Top 10 categorias por vendas (mais informativo que IDs)
        plt.figure(figsize=(10, 6))
        category_sales = (
            product_reco_stats.groupby("product_category_name")
            .agg(total_orders=("total_orders", "sum"))
            .sort_values("total_orders", ascending=False)
            .head(10)
            .iloc[::-1]
        )
        plt.barh(category_sales.index, category_sales["total_orders"])
        plt.title("Top 10 categorias mais vendidas (por numero de pedidos)")
        plt.xlabel("Total de pedidos (delivered)")
        plt.tight_layout()
        path = output_dir / "top10_categories_by_orders.png"
        plt.savefig(path)
        plt.close()
        figure_paths["top10_categories_by_orders"] = path

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
        plt.xticks(orders_by_year.index.astype(int))
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
        sns.heatmap(df_products[numeric_cols].corr(), annot=True, fmt=".2f", cmap="coolwarm")
        plt.title("Correlacao entre atributos fisicos dos produtos")
        plt.tight_layout()
        path = output_dir / "products_numeric_corr.png"
        plt.savefig(path)
        plt.close()
        figure_paths["products_numeric_corr"] = path

    # ========== VISUALIZACOES ADICIONAIS ==========

    # 6. Pedidos por mes (evolucao temporal) - corte em 2018-08
    if "order_purchase_timestamp" in df_orders.columns:
        df_orders_temp = df_orders.copy()
        df_orders_temp["order_purchase_timestamp"] = pd.to_datetime(
            df_orders_temp["order_purchase_timestamp"]
        )
        # Filtrar ate 2018-08 (dados incompletos apos essa data)
        df_orders_temp = df_orders_temp[
            df_orders_temp["order_purchase_timestamp"] < "2018-09-01"
        ]
        df_orders_temp["year_month"] = df_orders_temp["order_purchase_timestamp"].dt.to_period("M")
        orders_by_month = df_orders_temp.groupby("year_month").size()

        plt.figure(figsize=(12, 5))
        plt.plot(orders_by_month.index.astype(str), orders_by_month.values, marker="o", linewidth=2, color="steelblue")
        plt.title("Evolucao mensal de pedidos (2016-2018)")
        plt.xlabel("Mes/Ano")
        plt.ylabel("Quantidade de pedidos")
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        path = output_dir / "orders_by_month.png"
        plt.savefig(path)
        plt.close()
        figure_paths["orders_by_month"] = path

    # 7. Status dos pedidos (grafico de barras horizontal - mais legivel)
    if "order_status" in df_orders.columns:
        plt.figure(figsize=(10, 6))
        status_counts = df_orders["order_status"].value_counts()
        colors = sns.color_palette("Set2", len(status_counts))
        bars = plt.barh(status_counts.index, status_counts.values, color=colors)
        plt.title("Distribuicao de status dos pedidos")
        plt.xlabel("Quantidade de pedidos")
        plt.ylabel("Status")
        # Adicionar valores nas barras
        for bar, value in zip(bars, status_counts.values):
            percentage = (value / status_counts.sum()) * 100
            plt.text(value + 500, bar.get_y() + bar.get_height()/2, 
                     f"{value:,} ({percentage:.1f}%)", va="center", fontsize=9)
        plt.tight_layout()
        path = output_dir / "order_status_distribution.png"
        plt.savefig(path)
        plt.close()
        figure_paths["order_status_distribution"] = path

    # 9. Receita por categoria (top 10)
    if not product_reco_stats.empty:
        plt.figure(figsize=(10, 6))
        revenue_by_cat = (
            product_reco_stats.groupby("product_category_name")["total_revenue"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .iloc[::-1]
        )
        colors = sns.color_palette("rocket", len(revenue_by_cat))
        plt.barh(revenue_by_cat.index, revenue_by_cat.values, color=colors)
        plt.title("Top 10 categorias por receita total (R$)")
        plt.xlabel("Receita total (R$)")
        plt.tight_layout()
        path = output_dir / "top10_categories_by_revenue.png"
        plt.savefig(path)
        plt.close()
        figure_paths["top10_categories_by_revenue"] = path

    # 10. Distribuicao de precos dos produtos
    if "price" in df_order_items.columns:
        plt.figure(figsize=(10, 5))
        prices = df_order_items["price"]
        prices_filtered = prices[prices <= prices.quantile(0.95)]  # Remove outliers
        plt.hist(prices_filtered, bins=50, edgecolor="black", alpha=0.7, color="steelblue")
        plt.title("Distribuicao de precos dos produtos (ate percentil 95)")
        plt.xlabel("Preco (R$)")
        plt.ylabel("Frequencia")
        plt.axvline(prices_filtered.mean(), color="red", linestyle="--", label=f"Media: R${prices_filtered.mean():.2f}")
        plt.axvline(prices_filtered.median(), color="green", linestyle="--", label=f"Mediana: R${prices_filtered.median():.2f}")
        plt.legend()
        plt.tight_layout()
        path = output_dir / "price_distribution.png"
        plt.savefig(path)
        plt.close()
        figure_paths["price_distribution"] = path

    print("\nVisualizacoes salvas em:", output_dir)
    for name, path in figure_paths.items():
        print(f"  - {name}: {path}")

    return figure_paths
