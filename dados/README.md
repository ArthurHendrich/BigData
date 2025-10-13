# Dicionário de Dados - Camada Bronze

## 📊 Datasets Disponíveis

Esta pasta contém os dados brutos (Bronze Layer) do Brazilian E-Commerce Public Dataset by Olist.

---

## 1. olist_customers_dataset.csv

**Descrição**: Informações sobre clientes da plataforma Olist.

**Total de Registros**: 99,441  
**Total de Colunas**: 5

### Estrutura

| Coluna | Tipo | Descrição | Exemplo |
|--------|------|-----------|---------|
| `customer_id` | string | Identificador único do cliente por pedido | "06b8999e2fba1a1fbc88172c00ba8bc7" |
| `customer_unique_id` | string | Identificador único do cliente (pode ter múltiplos pedidos) | "861eff4711a542e4b93843c6dd7febb0" |
| `customer_zip_code_prefix` | integer | Prefixo do CEP (5 primeiros dígitos) | 14409 |
| `customer_city` | string | Nome da cidade | "sao paulo" |
| `customer_state` | string | Sigla do estado (UF) | "SP" |

### Qualidade dos Dados

- ✅ **Valores Nulos**: 0
- ✅ **Duplicatas**: 0
- ✅ **Integridade**: 100%

### Observações

- `customer_id` é único por pedido, então um cliente pode aparecer múltiplas vezes
- `customer_unique_id` agrupa todos os pedidos do mesmo cliente
- CEP está truncado (apenas prefixo) por privacidade
- Nomes de cidades estão em lowercase sem acentuação

---

## 2. olist_products_dataset.csv

**Descrição**: Catálogo de produtos disponíveis na plataforma Olist.

**Total de Registros**: 32,951  
**Total de Colunas**: 9

### Estrutura

| Coluna | Tipo | Descrição | Exemplo | Unidade |
|--------|------|-----------|---------|---------|
| `product_id` | string | Identificador único do produto | "1e9e8ef04dbcff4541ed26657ea517e5" | - |
| `product_category_name` | string | Categoria do produto (em português) | "perfumaria" | - |
| `product_name_lenght` | integer | Comprimento do nome do produto | 40 | caracteres |
| `product_description_lenght` | integer | Comprimento da descrição | 287 | caracteres |
| `product_photos_qty` | integer | Quantidade de fotos do produto | 1 | fotos |
| `product_weight_g` | integer | Peso do produto | 225 | gramas |
| `product_length_cm` | integer | Comprimento da embalagem | 16 | centímetros |
| `product_height_cm` | integer | Altura da embalagem | 10 | centímetros |
| `product_width_cm` | integer | Largura da embalagem | 14 | centímetros |

### Qualidade dos Dados

- ⚠️ **Valores Nulos**: ~600 em `product_category_name`
- ✅ **Duplicatas**: 0
- ✅ **Integridade**: ~98%

### Observações

- Dimensões referem-se à **embalagem**, não ao produto em si
- Categorias estão em **português brasileiro**
- Alguns produtos não têm categoria definida (nulos)
- Não há informação de **preço** neste dataset
- Peso está em gramas, dimensões em centímetros

### Categorias Principais

As categorias mais comuns incluem:
- `cama_mesa_banho` (cama, mesa e banho)
- `beleza_saude` (beleza e saúde)
- `esporte_lazer` (esporte e lazer)
- `informatica_acessorios` (informática)
- `moveis_decoracao` (móveis e decoração)
- `utilidades_domesticas` (utilidades domésticas)
- *[... e muitas outras]*

---

## 📐 Features Derivadas (Planejadas para Silver Layer)

A partir destes dados, planejamos criar:

### Customers
- `region`: Região do Brasil (Sul, Sudeste, etc.) baseada no estado
- `city_normalized`: Cidade com acentuação correta
- `is_capital`: Boolean indicando se é capital

### Products
- `volume_cm3`: Comprimento × Altura × Largura (volume da embalagem)
- `density`: Peso / Volume (densidade)
- `has_category`: Boolean (True se categoria não for nula)
- `category_encoded`: Encoding numérico das categorias
- `size_category`: Small/Medium/Large baseado em volume

---

## 🔗 Relacionamentos entre Datasets

Para análises completas, estes datasets podem ser combinados com outros datasets Olist:

```
customers ──1:N── orders ──1:N── order_items ──N:1── products
```

**Nota**: No escopo atual do projeto (AV1), estamos focando apenas em análises descritivas de clientes e produtos separadamente. Análises de vendas serão adicionadas em fases futuras.

---

## 📈 Casos de Uso

### Com Customers Dataset
- Distribuição geográfica de clientes
- Análise de concentração por estado/cidade
- Segmentação regional
- Identificação de mercados principais

### Com Products Dataset
- Catálogo de produtos por categoria
- Análise de dimensões e pesos
- Perfil de embalagens
- Diversidade de categorias

---

## 🔄 Processo de Atualização

**Fonte Original**: [Kaggle - Brazilian E-Commerce Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)  
**Última Atualização**: Outubro 2024  
**Frequência**: Dataset estático (histórico, sem atualizações periódicas)

---

## ⚠️ Limitações Conhecidas

1. **Sem preços**: Dataset de produtos não inclui valores
2. **CEP truncado**: Apenas prefixo disponível (5 dígitos)
3. **Categorias em português**: Requer tradução para uso internacional
4. **Categorias nulas**: ~600 produtos sem categoria definida
5. **Sem timestamps**: Não há datas de cadastro ou última modificação

---

## 📝 Changelog

### v1.0 - Outubro 2024
- Ingestão inicial dos datasets
- Análise de qualidade de dados
- Documentação criada

---

**Responsável pela curadoria**: Henrique Cordeiro - Engenheiro de Dados  
**Instituição**: CESAR School
