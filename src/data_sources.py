from dataclasses import dataclass
from typing import List
from . import config


@dataclass
class DataSource:
    name: str
    description: str
    file_name: str
    layer: str = "bronze"
    format: str = "csv"


def get_data_sources() -> List[DataSource]:

    return [
        DataSource(
            name="Customers",
            description="Cadastro de clientes: IDs, cidade, estado, CEP, etc.",
            file_name=config.CUSTOMERS_FILE,
        ),
        DataSource(
            name="Orders",
            description="Pedidos realizados na plataforma: status, timestamps, cliente.",
            file_name=config.ORDERS_FILE,
        ),
        DataSource(
            name="Order Items",
            description="Itens de cada pedido: produto, preço, quantidade.",
            file_name=config.ORDER_ITEMS_FILE,
        ),
        DataSource(
            name="Products",
            description="Catálogo de produtos: categoria, dimensões, peso, etc.",
            file_name=config.PRODUCTS_FILE,
        ),
    ]


def describe_sources() -> None:
    print("Fontes de Dados do Projeto (Olist E-commerce):\n")
    for src in get_data_sources():
        print(f"- {src.name}")
        print(f"  Descrição : {src.description}")
        print(f"  Arquivo   : {src.file_name}")
        print(f"  Camada    : {src.layer}")
        print(f"  Formato   : {src.format}")
        print()
