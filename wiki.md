# SUS Data Explorer - Wiki

Bem-vindo à Wiki do SUS Data Explorer! Aqui você encontrará informações detalhadas sobre o projeto, como utilizá-lo e como contribuir.

## Sobre o Projeto

O SUS Data Explorer é um sistema **AI first, mobile first, community first** para buscar, unificar e servir dados oficiais do SUS, começando pela pesquisa "Avaliação da efetividade da Rede de Atenção às Urgências no Estado da Bahia (2013-2023)".

### Missão & Visão

**Construir um OSS resiliente** que simplifique o acesso aos bancos públicos do SUS, gere insights reproduzíveis e permita evolução colaborativa.

**Meta Fase 1:** entregar todos os indicadores de estrutura, processo e resultado, filtráveis por Região de Saúde/município e exportáveis (CSV/Parquet/JSON).

## Como Contribuir

Nós adoraríamos receber sua contribuição para o SUS Data Explorer! Existem várias maneiras de contribuir:

### 1. Contribuindo com Código

Para contribuir com código:

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nome-da-feature`)
3. Implemente suas mudanças
4. Adicione testes para suas mudanças
5. Execute os testes para garantir que tudo está funcionando
6. Faça commit das suas mudanças (`git commit -m 'Adiciona nova feature'`)
7. Envie para o GitHub (`git push origin feature/nome-da-feature`)
8. Abra um Pull Request

Para mais detalhes, consulte nosso [guia de contribuição](../CONTRIBUTING.md).

### 2. Reportando Bugs

Se você encontrar um bug, por favor, abra uma issue usando o template de bug report. Inclua:

- Uma descrição clara do problema
- Passos para reproduzir o bug
- Comportamento esperado vs. comportamento observado
- Capturas de tela, se aplicável
- Informações sobre seu ambiente (sistema operacional, versão do Python, etc.)

### 3. Sugerindo Melhorias

Para sugerir melhorias ou novos recursos, abra uma issue usando o template de feature request. Descreva:

- O que você gostaria de ver implementado
- Por que isso seria útil para o projeto
- Como você imagina que isso funcionaria

### 4. Solicitando Novos Datasets

Se você precisa de acesso a um dataset específico do SUS que ainda não está disponível no projeto, abra uma issue usando o template de dataset-request.

## Configuração do Ambiente de Desenvolvimento

### Requisitos

- Python 3.10 ou superior
- Poetry para gerenciamento de dependências

### Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/sus-data-explorer.git
cd sus-data-explorer

# Instale as dependências com Poetry
poetry install

# Ative o ambiente virtual
poetry shell
```

### Executando a API

```bash
# Execute a API
python -m api.main
```

### Executando a CLI

```bash
# Liste as fontes de dados disponíveis
python api/cli.py sources

# Liste os datasets disponíveis
python api/cli.py datasets

# Busque dados
python api/cli.py pull ckan dataset_id --region 290001 --years 2013:2023
```

### Executando o App Mobile

```bash
# Entre no diretório do app
cd mobile/app

# Instale as dependências
npm install

# Inicie o app
npm start
```

## Estrutura do Projeto

```
sus-data-explorer/
├── connectors/       # Conectores para fontes de dados
│   ├── base.py       # Classe base para conectores
│   ├── ckan.py       # Conector para CKAN OpenDataSUS
│   ├── demas.py      # Conector para DEMAS
│   ├── tabnet.py     # Conector para DATASUS TABNET
│   └── egestor.py    # Conector para e-Gestor AB
├── api/              # API FastAPI e CLI
│   ├── main.py       # API FastAPI
│   └── cli.py        # Interface de linha de comando
├── mobile/           # Aplicativo mobile
│   └── app/          # App React Native
├── notebooks/        # Notebooks de análise
│   └── iam_bahia.ipynb  # Notebook da pesquisa IAM-Bahia
├── tests/            # Testes automatizados
└── docs/             # Documentação
```

## Fontes de Dados

O SUS Data Explorer integra dados das seguintes fontes:

1. **CKAN OpenDataSUS** - Datasets em CSV/Parquet (ex.: PNI, SIM, SIH)
2. **DEMAS / apidadosabertos.saude.gov.br** - CNES, leitos, estabelecimentos
3. **DATASUS TABNET** - Endpoints HTTP + downloads DBC via PySUS
4. **e-Gestor AB** - Dados da Atenção Básica via scraping

## Licença

Este projeto é licenciado sob a licença MIT - veja o arquivo [LICENSE](../LICENSE) para detalhes.
