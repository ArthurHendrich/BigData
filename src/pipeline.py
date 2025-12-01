"""

Orquestração do pipeline de Big Data (batch) para o dataset da Olist.

Etapas:
1. Fontes de Dados (descritas em data_sources.py)
2. Ingestão (batch) -> Bronze (ingestion.py)
3. Transformação -> Silver (transformation.py)
4. Carregamento -> salva Silver e Gold
5. Destino -> arquivos CSV/Parquet em /dados/{bronze,silver,gold}
               + notebooks / dashboards que consomem essas camadas
"""

from datetime import datetime

from . import ingestion, transformation, gold_metrics, data_sources, config, visualizations


def run_full_pipeline() -> None:
    """
    Executa o pipeline completo de ponta a ponta.
    """
    print("=================================================================")
    print("  OLIST E-COMMERCE DATA PIPELINE  (BRONZE / SILVER / GOLD)")
    print("=================================================================\n")

    print("Etapa 1 - Fontes de Dados (Data Sources)")
    data_sources.describe_sources()

    print("Etapa 2 - Ingestão (Ingestion) - Batch -> Bronze")
    dfs_bronze = ingestion.ingest_bronze()

    print("\nEtapa 3 - Transformação (Transformation) -> Silver")
    dfs_silver = transformation.transform_to_silver(dfs_bronze)

    print("\nEtapa 4 & 5 - Carregamento + Destino (Loading + Destination) -> Gold")
    products_by_category, customers_by_region, product_reco_stats = gold_metrics.build_gold_tables(
        dfs_silver
    )

    print("\nEtapa 6 - Visualizações (dashboards e gráficos)")
    figure_paths = visualizations.generate_all_visualizations(
        dfs_silver,
        products_by_category,
        customers_by_region,
        product_reco_stats,
    )

    print("\n================= PIPELINE SUMMARY =================")
    print(f"Execution timestamp : {datetime.now().isoformat(timespec='seconds')}")
    print(f"Bronze dir          : {config.BRONZE_DIR}")
    print(f"Silver dir          : {config.SILVER_DIR}")
    print(f"Gold dir            : {config.GOLD_DIR}")
    print("Gold files          :")
    print("  - gold_category_analysis.csv")
    print("  - gold_customers_by_region.csv")
    print("  - gold_product_recommendation_stats.csv")
    print("  - gold_customer_category_history.csv")
    print("  - gold_top_insights.csv")
    print("Figures (visualizations):")
    for name, path in figure_paths.items():
        print(f"  - {name}: {path}")
    print("====================================================\n")

    print("Top categorias de produto (amostra):")
    if not products_by_category.empty:
        print(products_by_category.head(5))
    else:
        print("  [No category data]")

    print("\nTop categorias de produtos mais vendidos (amostra):")
    if not product_reco_stats.empty:
        print(product_reco_stats[["product_id", "product_category_name", "total_orders"]].head(5))
    else:
        print("  [No recommendation stats]")

    print("\n✅ Pipeline concluído com sucesso!")


if __name__ == "__main__":
    run_full_pipeline()
