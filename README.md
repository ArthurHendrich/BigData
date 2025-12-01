## 1. Introdução

O avanço acelerado do comércio eletrônico tem ampliado significativamente o volume, a variedade e a velocidade com que dados são gerados e armazenados pelas plataformas digitais. Transações, registros de navegação, características de produtos, comportamentos de compra e informações de clientes constituem um ecossistema informacional complexo, cuja exploração adequada representa um diferencial competitivo essencial para empresas do setor. Entretanto, grande parte desses dados encontra-se distribuída em múltiplas fontes, heterogênea em formato e qualidade, o que dificulta sua utilização direta em processos analíticos e modelos de suporte à decisão.

Nesse contexto, a construção de pipelines de Big Data se torna uma estratégia fundamental para viabilizar o tratamento sistemático desses conjuntos massivos de informações. Um pipeline bem estruturado permite a coleta, organização, padronização e enriquecimento dos dados, assegurando governança, rastreabilidade e preparação adequada para análises avançadas. A necessidade de arquiteturas eficientes — capazes de lidar com operações de ingestão, transformação, integração e disponibilização de dados — é particularmente relevante quando se considera a aplicação de sistemas de recomendação, que dependem da qualidade e consistência dos dados para gerar valor.

Este projeto aborda esse desafio ao desenvolver um pipeline completo de Big Data aplicado ao dataset público brasileiro **Olist**, amplamente utilizado em estudos de e-commerce por sua riqueza de informações sobre clientes, pedidos, produtos e itens comprados. A proposta consiste em transformar dados brutos em insights estruturados, empregando a **Arquitetura Medallion** (Bronze, Silver e Gold) como referência para organizar o fluxo de processamento. O problema central investigado reside na necessidade de integrar diferentes tabelas, corrigir inconsistências, padronizar atributos e gerar métricas capazes de apoiar análises sobre comportamento de consumidores, categorias de produtos e potencial aplicação futura em sistemas de recomendação.

Assim, a introdução deste trabalho fundamenta a relevância do desenvolvimento de pipelines robustos para ambientes de e-commerce e estabelece o ponto de partida para a metodologia empregada, que busca transformar dados dispersos e despadronizados em informações estratégicas e analiticamente úteis.

---

## **2. Motivação**

A motivação para o desenvolvimento deste pipeline fundamenta-se em três elementos principais:  
(1) A relevância de sistemas de recomendação para aumentar conversões, retenção e personalização no E-commerce;  
(2) A riqueza e diversidade do dataset da Olist, que fornece um ambiente realista e variado para estudos acadêmicos;  
(3) A necessidade de aplicar práticas profissionais de Engenharia de Dados, utilizando camadas estruturadas (Bronze, Silver e Gold) que refletem arquiteturas adotadas em ambientes corporativos. Dessa forma, o projeto une relevância prática, aplicabilidade acadêmica e a oportunidade de consolidar técnicas essenciais do processamento de dados em larga escala.

---

## **3. Objetivo do Projeto**

O objetivo geral é construir um pipeline de Big Data em modo batch, capaz de processar, transformar e consolidar dados de E-commerce em estruturas analíticas adequadas para estudos exploratórios e geração de métricas de recomendação.

### **Objetivos específicos**

- Organizar os dados brutos em uma camada Bronze.
- Aplicar transformações, limpezas e enriquecimentos na camada Silver.
- Gerar métricas de negócio e tabelas de recomendação na camada Gold.
- Criar visualizações que revelem padrões relevantes para análise.
- Estruturar o repositório e documentação conforme diretrizes da disciplina.

---

## **4. Metodologia (Pipeline de Dados)**

A metodologia segue a arquitetura em camadas do tipo **Bronze → Silver → Gold**, amplamente utilizada em Engenharia de Dados. O pipeline foi construído em Python utilizando as bibliotecas `pandas`, `numpy`, `pyarrow`, `matplotlib` e `seaborn`. A organização do repositório inclui pastas específicas para código (`/src`), notebooks (`/notebooks`) e dados processados (`/dados`).

### **4.1 Fontes de Dados**

As fontes utilizadas pertencem ao _Brazilian E-Commerce Public Dataset by Olist_, contendo tabelas como:

- **Customers** — informações de cadastro e localização;
- **Orders** — status, datas e eventos dos pedidos;
- **Order Items** — produtos adquiridos e valores;
- **Products** — catálogo e atributos físicos.  
  Os arquivos originais são estruturados em formato CSV e armazenados na camada Bronze.

### **4.2 Ingestão**

A ingestão ocorre em modo batch utilizando `pandas.read_csv`. Nesta etapa, os dados são importados sem alterações e armazenados em `/dados/bronze/`.  
A ingestão também envolve validação básica de formatos e dimensões das tabelas.

### **4.3 Transformação**

A transformação, executada na camada Silver, inclui:

- limpeza de nulos;
- remoção de duplicados;
- padronização de texto;
- conversão de datas;
- criação de colunas derivadas (densidade, volume, região do cliente etc.).

Os arquivos resultantes são salvos em CSV e Parquet para maior eficiência e normalização.

### **4.4 Carregamento**

Os dados transformados são estruturados e consolidados para composição da camada Gold, garantindo padronização e consistência. O carregamento define o formato final dos arquivos disponibilizados para análise.

### **4.5 Destino (Camada Gold)**

A camada Gold reúne métricas avançadas de negócio e estruturações direcionadas a sistemas de recomendação, incluindo:

- análise de categorias;
- distribuição de clientes por região;
- métricas de popularidade de produtos;
- histórico de compras por categoria;
- indicadores consolidados para insights estratégicos.

Os resultados são armazenados em `/dados/gold/` em arquivos CSV e Parquet.

---

## **5. Resultados e Visualizações**

As análises e gráficos foram desenvolvidos no notebook `pipeline_olist.ipynb`, localizado em `/notebooks`. Entre os principais resultados observados estão:

- concentração de clientes na região Sudeste;
- categorias com maior número de produtos e maior volume de vendas;
- identificação de produtos mais populares por receita e frequência;
- padrões temporais recorrentes nos horários de compra;
- distribuição de preços e atributos físicos dos produtos.

As visualizações geradas incluem:

- gráficos de barras, histogramas e boxplots;
- heatmaps de correlação;
- análises de tendência e distribuição;
- tabelas de insights extraídos da camada Gold.

Esses resultados oferecem base sólida para aplicações futuras em modelos de filtragem colaborativa ou recomendação baseada em conteúdo.

---

## **6. Conclusões**

O pipeline desenvolvido cumpre os requisitos propostos, demonstrando a viabilidade de estruturar dados em múltiplas camadas e extrair valor analítico de um ambiente realista de E-commerce. A metodologia aplicada evidenciou a importância de processos bem definidos para garantir qualidade e rastreabilidade dos dados.

### **Principais conclusões**

- A arquitetura Bronze–Silver–Gold favorece clareza e organização.
- O dataset, apesar de heterogêneo, oferece amplo potencial analítico.
- As métricas geradas fornecem insumos para sistemas de recomendação.

### **Dificuldades encontradas**

- alta fragmentação de categorias de produtos;
- integração entre múltiplas tabelas com chaves distintas;
- presença de registros incompletos ou inconsistentes.

### **Trabalhos futuros**

- implementação de recomendadores colaborativos;
- inclusão de ingestão por streaming;
- uso de dashboards interativos (Dash, PowerBI);
- enriquecimento dos dados com mapas geográficos externos;
- aplicação de técnicas de machine learning para clusterização de clientes.

---
