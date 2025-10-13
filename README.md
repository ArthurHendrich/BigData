# Pipeline de Big Data - Análise de E-commerce Olist

## Descrição do Projeto

Este projeto implementa um pipeline completo de Big Data para análise de dados de e-commerce da plataforma brasileira **Olist**. O objetivo é transformar dados brutos de clientes e produtos em insights estratégicos que possam auxiliar na tomada de decisões de negócio.

O projeto utiliza a **Arquitetura Medallion** (Bronze, Silver, Gold) para organizar o fluxo de dados, garantindo qualidade, governança e preparação adequada dos dados para análises avançadas.

## Problema a Resolver

Empresas de e-commerce lidam com grandes volumes de dados diariamente, mas muitas vezes esses dados estão dispersos, desorganizados e não são aproveitados adequadamente. O desafio é:

- **Integrar** dados de múltiplas fontes (clientes, produtos)
- **Limpar e transformar** dados brutos em informações confiáveis
- **Gerar insights** acionáveis sobre vendas, segmentação de clientes e comportamento de mercado
- **Otimizar** processos de negócio através de análise de dados

## Fonte dos Dados

**Dataset**: Brazilian E-Commerce Public Dataset by Olist  
**Fonte**: [Kaggle - Olist E-Commerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

**Datasets utilizados**:

- `olist_customers_dataset.csv`
- `olist_products_dataset.csv`

### Pipeline Implementado

1. **Ingestão**: Download de datasets do Kaggle → Upload no Google Colab
2. **Armazenamento Bronze**: CSV bruto (formato original)
3. **Transformação Silver**: Limpeza, normalização, enriquecimento
4. **Armazenamento Gold**: Dados agregados prontos para visualização
5. **Análise**: Notebooks Jupyter com visualizações e insights

## Ferramentas Utilizadas

- **Python 3.x** - Linguagem principal
- **Pandas** - Manipulação e análise de dados
- **NumPy** - Operações numéricas
- **Matplotlib/Seaborn** - Visualização de dados
- **Plotly** - Gráficos interativos
- **Google Colab** - Ambiente de desenvolvimento
- **GitHub** - Versionamento de código
- **Jupyter Notebook** - Documentação e análise

## Equipe e Divisão de Tarefas

### Integrantes

- **Arthur Henrich** - aham@cesar.school
- **Henrique Cordeiro** - hcp@cesar.school
- **Luiza Omena** - los2@cesar.school

## Como Executar

### Pré-requisitos

- Python 3.7+
- Google Colab (recomendado) ou Jupyter Notebook local

### Passo a Passo

1. **Clone o repositório**:

```bash
git clone https://github.com/ArthurHendrich/BigData.git
cd BigData
```

2. **Instale as dependências**:

```bash
pip install pandas numpy matplotlib seaborn plotly scikit-learn
```

3. **Execute o notebook**:

- Abra `codigo/preProcessamento.ipynb` no Google Colab ou Jupyter
- Execute as células sequencialmente
- Os dados serão processados através das camadas Bronze → Silver → Gold

4. **link do colab**:
   https://colab.research.google.com/drive/1Q3HkqvHgv-x1Mmxw2PgC6ZlrqnzdtSDd?usp=sharing
