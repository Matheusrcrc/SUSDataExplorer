# SUS Data Explorer

Sistema **AI first, mobile first, community first** para buscar, unificar e servir dados oficiais do SUS, começando pela pesquisa "Avaliação da efetividade da Rede de Atenção às Urgências no Estado da Bahia (2013-2023)".

## Missão & Visão

**Construir um OSS resiliente** que simplifique o acesso aos bancos públicos do SUS, gere insights reproduzíveis e permita evolução colaborativa.

**Meta Fase 1:** entregar todos os indicadores de estrutura, processo e resultado descritos no anexo, filtráveis por Região de Saúde/município e exportáveis (CSV/Parquet/JSON).

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

## Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/sus-data-explorer.git
cd sus-data-explorer

# Instale as dependências com Poetry
poetry install
```

## Uso

```bash
# Ative o ambiente virtual
poetry shell

# Execute a API
python -m api.main

# Use a CLI para buscar dados
susx pull ckan --region 290001 --years 2013:2023
```

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

- **Backend**: Python 3.10, FastAPI, AsyncIO, Pydantic, SQLModel, Redis cache
- **Data layer**: DuckDB + Parquet para portabilidade
- **ETL helpers**: PySUS, pandas, polars, httpx, orjson
- **Testes**: pytest, coverage >90%, contract tests nos conectores

## Contribuição

Contribuições são bem-vindas! Por favor, leia o [guia de contribuição](CONTRIBUTING.md) para mais detalhes.

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.
