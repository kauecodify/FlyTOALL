# FlyTOALL

<img width="1342" height="661" alt="image" src="https://github.com/user-attachments/assets/2f2ad7e0-030e-4485-8d5c-e2230e4ea589" />

### Real-Time Data Workspace & Predictive Intelligence

O **FLYTOALL** é uma plataforma SaaS para gerenciamento, análise e previsão de dados operacionais em tempo real.

A plataforma transforma planilhas e bases estruturadas em um ambiente interativo de **Data Management, Analytics e Predictive Intelligence**, permitindo que usuários definam colunas-alvo, acompanhem tendências e gerem previsões automaticamente.

---

## Visão

Empresas ainda dependem fortemente de planilhas para acompanhar vendas, estoque, logística, produção, financeiro e operações.

O FLYTOALL transforma esse fluxo:

```text
PLANILHA
   ↓
FLYTOALL
   ↓
TRATAMENTO DOS DADOS
   ↓
SELEÇÃO DAS VARIÁVEIS-ALVO
   ↓
ANÁLISE ESTATÍSTICA
   ↓
PREVISÃO
   ↓
DECISÃO OPERACIONAL
```

A proposta é criar uma camada de inteligência entre os dados operacionais e a tomada de decisão.

---

# Principais funcionalidades

## Gestão de dados

* Upload de arquivos CSV
* Upload de arquivos XLSX
* Importação de dados estruturados
* Visualização em formato de tabela
* Edição de células
* Adição de novas linhas
* Adição de novas colunas
* Atualização dos dados em tempo real

---

## Target Columns

O usuário pode selecionar uma ou várias **colunas-alvo** para análise.

Exemplo:

```text
Data
Produto
Região
Vendas       ← TARGET
Estoque
Preço
```

O FLYTOALL utiliza a coluna selecionada como variável de interesse para gerar análises e previsões.

É possível trabalhar com múltiplos targets:

```text
TARGETS

✓ Vendas
✓ Estoque
✓ Receita
□ Custos
□ Pedidos
```

---

# Predictive Intelligence

O núcleo atual utiliza **Regressão Linear** para identificar relações e tendências nos dados.

Para cada variável-alvo, o sistema pode apresentar:

* Valor atual
* Tendência
* Inclinação da série
* R²
* Previsões futuras
* Histórico utilizado no modelo

Exemplo:

```text
Vendas

Atual:       10.420
Tendência:   ↑ Crescente
R²:          0.94

Próximas previsões:

T+1 → 10.680
T+2 → 10.930
T+3 → 11.210
T+4 → 11.480
T+5 → 11.760
```

> As previsões são modelos estatísticos e não garantem resultados futuros. A qualidade depende da estrutura, quantidade e qualidade dos dados utilizados.

---

# Real-Time Workspace

O FLYTOALL possui comunicação em tempo real utilizando **WebSockets**.

Quando os dados são alterados, o sistema pode sincronizar o estado e atualizar as análises.

Arquitetura simplificada:

```text
Browser
   │
   │ WebSocket
   ▼
FastAPI
   │
   ├── Data Engine
   │
   ├── Forecast Engine
   │
   └── Analytics
```

---

# Aplicações práticas

O FLYTOALL pode ser utilizado em diferentes áreas.

### Estoque

Previsão de demanda e acompanhamento de níveis de estoque.

### Logística

Análise de volume de entregas, pedidos, atrasos e capacidade operacional.

### Varejo e Atacado

Previsão de vendas por produto, região, período ou canal.

### Indústria

Análise de produção, consumo de recursos e comportamento operacional.

### Financeiro

Análise de receitas, despesas, custos e indicadores financeiros.

### Comercial

Acompanhamento de vendas, conversão, metas e desempenho.

### Recursos Humanos

Análise de produtividade, absenteísmo e indicadores de equipes.

### Dados financeiros e risco

Análise de indicadores e identificação de tendências em bases financeiras.

---

# Exemplo de utilização

Uma empresa possui uma planilha de vendas:

```text
Data       Produto    Região    Vendas    Estoque
01/09      Arroz      SP        820       5000
02/09      Arroz      SP        850       4700
03/09      Arroz      SP        910       4250
04/09      Arroz      SP        980       3800
05/09      Arroz      SP        1040      3300
```

O usuário importa a planilha e seleciona:

```text
Target:
Vendas
```

O FLYTOALL analisa a série disponível e gera uma projeção.

Ao mesmo tempo, o usuário pode acompanhar:

```text
Vendas       ↑
Estoque      ↓
Demanda      ↑
```

Isso permite identificar situações como:

> Crescimento das vendas combinado com redução do estoque.

A empresa pode então utilizar essa informação para avaliar decisões de abastecimento.

---

# Arquitetura

A versão atual foi construída como um SaaS experimental utilizando:

```text
                ┌───────────────────────┐
                │      FLYTOALL UI      │
                │ HTML / CSS / JavaScript│
                └───────────┬───────────┘
                            │
                     REST / WebSocket
                            │
                ┌───────────▼───────────┐
                │        FastAPI        │
                └───────────┬───────────┘
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
        Data Engine   Forecast Engine   Analytics
             │              │              │
             └──────────────┼──────────────┘
                            ▼
                    Prediction Results
```

---

# Stack

## Backend

* Python
* FastAPI
* Uvicorn
* Pandas
* NumPy
* Scikit-learn

## Frontend

* HTML5
* CSS3
* JavaScript
* WebSocket

## Machine Learning

* Linear Regression
* R²
* Trend Analysis
* Forecasting

---

# Estrutura

```text
FLYTOALL/
│
├── app.py
├── requirements.txt
├── README.md
│
└── static/
    └── index.html
```

---

# Instalação

Clone o projeto:

```bash
git clone <repository-url>
cd FLYTOALL
```

Crie um ambiente virtual:

```powershell
py -m venv .venv
```

Ative:

```powershell
.venv\Scripts\activate
```

Instale as dependências:

```powershell
pip install -r requirements.txt
```

Execute:

```powershell
uvicorn app:app --reload
```

Acesse:

```text
http://127.0.0.1:8000
```

---

# Formatos suportados

Atualmente:

```text
.csv
.xlsx
.xls
```

A plataforma transforma o conteúdo importado em uma estrutura tabular que pode ser editada e analisada.

---

# Fluxo do usuário

```text
1. Abrir o FLYTOALL
        ↓
2. Importar planilha
        ↓
3. Visualizar dados
        ↓
4. Editar / adicionar dados
        ↓
5. Selecionar coluna(s)-alvo
        ↓
6. Executar análise
        ↓
7. Visualizar tendências
        ↓
8. Visualizar previsão
        ↓
9. Exportar os dados
```

---

# Roadmap

## V1 — Data Workspace

* [x] Upload CSV
* [x] Upload XLSX
* [x] Tabela editável
* [x] Adicionar linhas
* [x] Adicionar colunas
* [x] Target Columns
* [x] Regressão Linear
* [x] Forecast
* [x] WebSocket
* [x] Exportação CSV

---

# Evolução da Inteligência Artificial

A Regressão Linear funciona como um **baseline** inicial.

A arquitetura pode evoluir para diferentes modelos e mecanismos de inteligência:

```text
Linear Regression
       ↓
Random Forest
       ↓
XGBoost
       ↓
Time Series Models
       ↓
Anomaly Detection
       ↓
Optimization Engine
       ↓
Generative AI
```

Possíveis evoluções:

* Previsão de demanda
* Detecção automática de anomalias
* Previsão de estoque
* Previsão de receita
* Classificação de riscos
* Detecção de gargalos
* Otimização de operações
* Recomendações automáticas
* Explicações geradas por IA

---

# Integração com sistemas corporativos

Em uma versão Enterprise, o FLYTOALL poderá funcionar como uma camada de inteligência conectada aos sistemas existentes.

```text
ERP
 │
 ├── Vendas
 ├── Compras
 ├── Financeiro
 └── Clientes
       │
       ▼
     FLYTOALL
       │
       ├── Analytics
       ├── Machine Learning
       ├── Forecasting
       └── Optimization
       │
       ▼
WMS ── TMS ── APIs ── Data Lake
```

O objetivo não é necessariamente substituir o ERP da empresa, mas adicionar uma camada analítica e preditiva sobre os dados existentes.

---

# Segurança e Governança

Para uma implantação corporativa, o projeto deverá evoluir para incluir:

* Autenticação
* Autorização
* RBAC
* Isolamento entre organizações
* Gestão de sessões
* Criptografia
* Gestão de secrets
* Logs de auditoria
* Monitoramento
* Backup
* Disaster Recovery
* Controle de acesso aos datasets
* Governança de modelos
* Monitoramento de model drift
* Adequação à LGPD

---

# Modelo de negócio

O FLYTOALL pode evoluir para um modelo SaaS B2B.

### Starter

Para pequenos negócios que trabalham principalmente com planilhas.

```text
Planilhas
Analytics
Forecast
Dashboards
```

### Professional

Para equipes de dados e operações.

```text
Multiusuário
Datasets persistentes
Dashboards
APIs
Histórico
Forecast avançado
```

### Enterprise

Para organizações com infraestrutura de dados própria.

```text
Multi-tenant
ERP / WMS / TMS
APIs
Kafka
Data Lake
RBAC
Auditoria
Governança
SLA
Machine Learning
Optimization Engine
```

---

# Objetivo do produto

O objetivo do FLYTOALL é transformar dados operacionais em informação acionável.

```text
DATA
 ↓
INFORMATION
 ↓
ANALYTICS
 ↓
PREDICTION
 ↓
DECISION
 ↓
OPTIMIZATION
```

A visão de longo prazo é transformar o FLYTOALL em uma plataforma de **inteligência operacional em tempo real**, capaz de conectar dados, modelos preditivos e processos empresariais em um único ambiente.

---

# Status

**Current Stage:** SaaS Prototype

**Core:** Data Management + Analytics + Predictive Forecasting

**Architecture:** FastAPI + WebSocket + Machine Learning

**Current Model:** Linear Regression

**Target Market:** B2B / Data / Operations / Retail / Wholesale / Logistics / Industry

---

# Licença

FLYTOALL.
