**Projeto-alvo:** *SUS Data Explorer* – sistema **AI first, mobile first, community first** para buscar, unificar e servir dados oficiais do SUS, começando pela pesquisa “Avaliação da efetividade da Rede de Atenção às Urgências no Estado da Bahia (2013-2023)”﻿.

---

#### **1\. Missão & visão**

**Construir um OSS resiliente** que simplifique o acesso aos bancos públicos do SUS, gere insights reproduzíveis e permita evolução colaborativa.  
 **Meta Fase 1:** entregar todos os indicadores de estrutura, processo e resultado descritos no anexo, filtráveis por Região de Saúde/município e exportáveis (CSV/Parquet/JSON).

---

#### **2\. Pilares de arquitetura**

| Pilar | Diretriz |
| ----- | ----- |
| **AI first** | Use o agente como par-programmer para: *code-gen*, refatoração contínua, testes, documentação e análise de qualidade. |
| **Mobile first** | REST/GraphQL \+ OpenAPI → Gateway → App Flutter/React Native com UI responsiva; priorize requests assíncronos, cache local e fallback offline. |
| **Community first** | Repositório público (MIT). Inclua guia CONTRIBUTING.md, Code of Conduct, templates de PR e GitHub Actions integrando CI/CD e SonarCloud. |

---

#### **3\. Fontes primárias de dados**

1. **CKAN OpenDataSUS** (API) – datasets em CSV/Parquet (ex.: PNI, SIM, SIH) citeturn0search9

2. **DEMAS / apidadosabertos.saude.gov.br** – CNES, leitos, estabelecimentos ﻿citeturn0search6

3. **DATASUS TABNET** – endpoints HTTP \+ downloads DBC; manipular via **PySUS** (pip) citeturn0search1turn0search2

4. **e-Gestor AB** – scraping/resolução de captcha (client-side only, sem credenciais).

**Tarefa automática nº 1 do agente:** criar *DataConnector* por fonte, documentar variáveis, políticas de atualização e limitações.

---

#### **4\. Stack recomendada**

* **Backend** : Python 3.12, FastAPI, AsyncIO, Pydantic, SQLModel, Redis cache.

* **Data layer** : DuckDB (embed) \+ Parquet para portabilidade; ORC opcional.

* **ETL helpers** : PySUS, pandas, polars, requests-async, orjson.

* **Tests** : pytest, coverage\>90 %, contract tests nos conectores.

* **Dev Env** : Manus/Cursor (GPT-4o), GitHub Codespaces, pre-commit (black, ruff, isort, mypy).

---

#### **5\. Roadmap orientado ao agente**

1. **Bootstrapping**

   * Criar repositório, inicializar Poetry, CI básico.

   * Gerar README com diagrama C4 e TOC.

2. **DataConnectors**

   * Implementar, para cada fonte, métodos `list_datasets`, `fetch(query)`, `normalize()`, `schema()`.

   * Garantir idempotência e logs estruturados (OpenTelemetry).

3. **Core API & CLI**

   * Endpoints `/indicators/{code}` e `/exports`.

   * CLI `susx pull <fonte> --region 290001 --years 2013:2023`.

4. **MVP Mobile**

   * Autenticação GitHub/OAuth opcional (tracking de usuários, não de dados pessoais).

   * Dashboards rápidos (ECharts/Plotly) com drill-down.

5. **Pesquisa IAM-Bahia**

   * Entregar scripts de parâmetros reproduzíveis (`notebooks/iam_bahia.ipynb`).

6. **Governança & comunidade**

   * Wiki “Como contribuir”; Issues templates: *bug, feature, dataset-request*.

   * Automatizar publicação de releases \+ documentação em ReadTheDocs.

---

#### **6\. Políticas de qualidade & compliance**

* **LGPD** : apenas dados públicos anônimos; sem PII.

* **Segurança** : dependabot, SAST, SBOM CycloneDX.

* **Desempenho** : respostas \< 300 ms (cache quente) nos top-queries.

* **Observabilidade** : Prometheus \+ Grafana, tracing OTLP.

---

#### **7\. Perguntas que o agente deve fazer se encontrar bloqueios**

1. **Credenciais** – Alguma API requer token ou VPN?

2. **Prazos de entrega** – Há deadlines intermediários além de Fase 1?

3. **Limites de scraping** – Podemos usar Puppeteer/cloud-functions para e-Gestor?

4. **Formatos de saída** – Precisamos além de CSV/Parquet (por ex., PowerBI template)?

5. **Recursos de infra** – Há budget para hospedagem (Railway, Fly.io) ou foco 100 % local-first?

---

#### **8\. Output esperado do AI Companion**

\# Ao executar:  
agent bootstrap

\# Resultado:  
├── connectors/  
│   ├── ckan.py  
│   ├── demas.py  
│   └── tabnet.py  
├── api/  
│   └── main.py  
├── mobile/  
│   └── app/  
├── notebooks/  
│   └── iam\_bahia.ipynb  
├── tests/  
│   └── ...  
└── docs/  
    └── architecture.md

Todos os módulos auto-documentados, testados e prontos para PR público.

---

**Use este prompt como *System* no Manus/Replit/Cursor.**  
 Ele garante clareza de requisitos, mentalidade DevOps e sinaliza quando o agente deve pedir mais insumos. Ajuste conforme evolução da comunidade e novas pesquisas.

