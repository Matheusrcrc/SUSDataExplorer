# 🏥 SUS Data Explorer

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

Sistema **AI first, mobile first, community first** para buscar, unificar e servir dados oficiais do SUS.

🌐 **[Demo Online](https://your-app.streamlit.app)** | 📖 **[Documentação](./DEPLOY.md)** | 🐛 **[Issues](../../issues)**

## 🎯 Missão & Visão

**Construir um OSS resiliente** que simplifique o acesso aos bancos públicos do SUS, gere insights reproduzíveis e permita evolução colaborativa.

**Meta Fase 1:** entregar todos os indicadores de estrutura, processo e resultado filtráveis por Região de Saúde/município e exportáveis (CSV/Parquet/JSON/Excel).

## Diagrama C4 - Visão Geral

```
+------------------------------------------+
|                                          |
|            SUS Data Explorer             |
|                                          |
+------------------------------------------+
                    |
        +-----------+-----------+
        |                       |
+-------v-------+      +--------v--------+
|               |      |                 |
| Frontend      |      | Backend         |
| Mobile-first  |<---->| FastAPI         |
| Flutter/React |      | Python          |
|               |      |                 |
+---------------+      +-----------------+
                              |
              +--------------+---------------+
              |              |               |
    +---------v----+ +-------v------+ +------v-------+
    |              | |              | |              |
    | CKAN         | | DEMAS        | | DATASUS      |
    | OpenDataSUS  | | API Dados    | | TABNET       |
    |              | | Abertos      | | PySUS        |
    +--------------+ +--------------+ +--------------+
```

## Índice

1. [Instalação](#instalação)
2. [Uso](#uso)
3. [Fontes de Dados](#fontes-de-dados)
4. [Arquitetura](#arquitetura)
5. [Contribuição](#contribuição)
6. [Licença](#licença)

## 🚀 Quick Start

### Opção 1: Usar a Aplicação Online (Recomendado)

Acesse: **[SUS Data Explorer App](https://your-app.streamlit.app)**

### Opção 2: Executar Localmente

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/SUSDataExplorer.git
cd SUSDataExplorer

# Crie um ambiente virtual e instale dependências
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Execute a aplicação Streamlit
streamlit run app_streamlit.py
```

A aplicação estará disponível em: `http://localhost:8501`

### Opção 3: Deploy Próprio

Veja o guia completo de deploy: **[DEPLOY.md](./DEPLOY.md)**

- Deploy no Streamlit Cloud (gratuito)
- Deploy no GitHub Pages (landing page)
- Configurações avançadas

## Fontes de Dados

O sistema integra dados das seguintes fontes:

1. **CKAN OpenDataSUS** - Datasets em CSV/Parquet (ex.: PNI, SIM, SIH)
2. **DEMAS / apidadosabertos.saude.gov.br** - CNES, leitos, estabelecimentos
3. **DATASUS TABNET** - Endpoints HTTP + downloads DBC via PySUS
4. **e-Gestor AB** - Dados obtidos via scraping

## Arquitetura

O projeto segue os princípios:

- **AI first**: Desenvolvimento assistido por IA para code-gen, refatoração, testes e documentação
- **Mobile first**: API REST/GraphQL com OpenAPI, gateway e app responsivo
- **Community first**: Repositório público com guias de contribuição e CI/CD integrado

### Stack Tecnológica

- **Frontend**: Streamlit (interface web interativa)
- **Backend**: Python 3.10+, AsyncIO
- **Data Processing**: Pandas, Plotly (visualizações)
- **Data Sources**: PySUS, httpx (APIs do SUS)
- **Deploy**: Streamlit Cloud (gratuito), GitHub Pages
- **Testes**: pytest, coverage >90%, contract tests nos conectores

### Funcionalidades da Aplicação

- 📊 Exploração interativa de dados do SUS
- 🔍 Filtros por região, município e período
- 📈 Visualizações com gráficos interativos (Plotly)
- 📥 Exportação em múltiplos formatos (CSV, JSON, Excel, Parquet)
- 🎨 Interface responsiva e acessível
- ⚡ Cache inteligente para performance

## Contribuição

Contribuições são bem-vindas! Por favor, leia o [guia de contribuição](CONTRIBUTING.md) para mais detalhes.

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.
