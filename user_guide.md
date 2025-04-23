# SUS Data Explorer - Documentação de Uso

## Introdução

O SUS Data Explorer é um sistema AI first, mobile first, community first para buscar, unificar e servir dados oficiais do SUS. Esta documentação fornece instruções detalhadas sobre como instalar, configurar e utilizar o sistema.

## Índice

1. [Instalação](#instalação)
2. [Configuração](#configuração)
3. [Utilizando a API](#utilizando-a-api)
4. [Utilizando a CLI](#utilizando-a-cli)
5. [Aplicativo Mobile](#aplicativo-mobile)
6. [Pesquisa IAM-Bahia](#pesquisa-iam-bahia)
7. [Contribuindo](#contribuindo)
8. [Solução de Problemas](#solução-de-problemas)

## Instalação

### Requisitos

- Python 3.10 ou superior
- Node.js 16 ou superior (para o aplicativo mobile)
- Acesso à internet para conexão com as APIs do SUS

### Instalação via Poetry

```bash
# Clone o repositório
git clone https://github.com/sus-data-explorer/sus-data-explorer.git
cd sus-data-explorer

# Instale as dependências com Poetry
poetry install
```

### Instalação via pip

```bash
# Clone o repositório
git clone https://github.com/sus-data-explorer/sus-data-explorer.git
cd sus-data-explorer

# Instale as dependências com pip
pip install -r requirements.txt
```

## Configuração

### Configuração da API

O SUS Data Explorer não requer configuração especial para a maioria das fontes de dados. No entanto, algumas fontes podem exigir autenticação:

1. Crie um arquivo `.env` na raiz do projeto:

```
# Credenciais para APIs que requerem autenticação
EGESTOR_USERNAME=seu_usuario
EGESTOR_PASSWORD=sua_senha
```

2. Configure o diretório de dados (opcional):

```
DATA_DIR=/caminho/para/diretorio/dados
```

### Configuração do Aplicativo Mobile

1. Navegue até o diretório do aplicativo:

```bash
cd mobile/app
```

2. Instale as dependências:

```bash
npm install
```

3. Configure as variáveis de ambiente:

```bash
cp .env.example .env
```

4. Edite o arquivo `.env` com o endereço da sua API:

```
API_URL=http://seu-servidor:8000
```

## Utilizando a API

A API do SUS Data Explorer fornece endpoints para acessar dados de diferentes fontes do SUS.

### Iniciando o servidor

```bash
cd sus-data-explorer
poetry run python -m api.main
```

O servidor será iniciado em `http://localhost:8000`.

### Endpoints Principais

#### Listar Fontes de Dados

```
GET /sources
```

Retorna todas as fontes de dados disponíveis.

#### Listar Datasets

```
GET /datasets
```

Retorna todos os datasets disponíveis em todas as fontes.

#### Listar Datasets por Fonte

```
GET /datasets/{source}
```

Retorna os datasets disponíveis em uma fonte específica.

Parâmetros:
- `source`: Fonte de dados (ckan, demas, tabnet, egestor)

#### Obter Dados de um Indicador

```
GET /indicators/{code}
```

Retorna dados de um indicador específico.

Parâmetros:
- `code`: Código do indicador
- `region`: Código IBGE da região ou município
- `start_year`: Ano inicial
- `end_year`: Ano final (opcional)
- `source`: Fonte de dados (opcional)

Exemplo:
```
GET /indicators/mortalidade?region=290001&start_year=2020&end_year=2022
```

#### Exportar Dados

```
GET /exports
```

Exporta dados de um indicador para um formato específico.

Parâmetros:
- `indicator`: Código do indicador
- `region`: Código IBGE da região ou município
- `start_year`: Ano inicial
- `end_year`: Ano final (opcional)
- `format`: Formato de exportação (csv, json, parquet)
- `source`: Fonte de dados (opcional)

Exemplo:
```
GET /exports?indicator=mortalidade&region=290001&start_year=2020&end_year=2022&format=csv
```

### Documentação Interativa

A API inclui documentação interativa gerada pelo Swagger UI, acessível em:

```
http://localhost:8000/docs
```

## Utilizando a CLI

A CLI do SUS Data Explorer permite acessar dados do SUS diretamente do terminal.

### Comandos Disponíveis

#### Informações sobre o SUS Data Explorer

```bash
python -m api.cli info
```

#### Listar Fontes de Dados

```bash
python -m api.cli list-sources
```

#### Listar Datasets

```bash
python -m api.cli list-datasets [fonte]
```

Parâmetros:
- `fonte`: (Opcional) Fonte de dados (ckan, demas, tabnet, egestor)

#### Obter Dados

```bash
python -m api.cli pull-data <fonte> <dataset> <região> <anos> <saída>
```

Parâmetros:
- `fonte`: Fonte de dados (ckan, demas, tabnet, egestor)
- `dataset`: ID do dataset
- `região`: Código IBGE da região ou município
- `anos`: Anos dos dados (formato: YYYY ou YYYY:YYYY)
- `saída`: Caminho do arquivo de saída (CSV, JSON, Parquet)

Exemplo:
```bash
python -m api.cli pull-data tabnet sim 290001 2020:2022 mortalidade_bahia.csv
```

## Aplicativo Mobile

O SUS Data Explorer inclui um aplicativo mobile desenvolvido com React Native.

### Executando o Aplicativo

```bash
cd mobile/app
npm start
```

### Funcionalidades do Aplicativo

- **Autenticação**: Login via GitHub OAuth
- **Exploração de Dados**: Navegação por fontes e datasets
- **Visualização**: Dashboards interativos com gráficos
- **Exportação**: Exportação de dados em diferentes formatos
- **Modo Offline**: Acesso a dados previamente baixados mesmo sem conexão

## Pesquisa IAM-Bahia

O SUS Data Explorer inclui um notebook Jupyter que implementa a pesquisa "Avaliação da efetividade da Rede de Atenção às Urgências no Estado da Bahia (2013-2023)".

### Executando o Notebook

```bash
cd sus-data-explorer
poetry run jupyter notebook notebooks/iam_bahia.ipynb
```

### Conteúdo do Notebook

O notebook `iam_bahia.ipynb` contém:

1. **Configuração do Ambiente**: Inicialização dos conectores e definição de parâmetros
2. **Coleta de Dados**: Obtenção de dados de diferentes fontes
3. **Análise de Indicadores**: Processamento e análise de indicadores de estrutura, processo e resultado
4. **Visualizações**: Gráficos e mapas para análise dos dados
5. **Conclusões**: Interpretação dos resultados e recomendações

## Contribuindo

O SUS Data Explorer é um projeto de código aberto e aceita contribuições da comunidade.

### Como Contribuir

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Faça commit das suas alterações (`git commit -m 'Adiciona nova feature'`)
4. Faça push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

Para mais detalhes, consulte o arquivo [CONTRIBUTING.md](CONTRIBUTING.md).

## Solução de Problemas

### Problemas Comuns

#### Erro de Conexão com APIs

Se você encontrar erros de conexão com as APIs do SUS, verifique:

1. Sua conexão com a internet
2. Se as APIs estão disponíveis (algumas APIs do SUS podem ficar indisponíveis temporariamente)
3. Se você está usando as credenciais corretas (quando aplicável)

#### Erro ao Executar o Aplicativo Mobile

Se o aplicativo mobile não iniciar corretamente:

1. Verifique se todas as dependências foram instaladas (`npm install`)
2. Verifique se o arquivo `.env` está configurado corretamente
3. Verifique se a API está em execução e acessível

#### Erro ao Executar o Notebook

Se o notebook não executar corretamente:

1. Verifique se o ambiente Python está configurado corretamente
2. Verifique se todas as dependências foram instaladas
3. Verifique se você tem acesso às fontes de dados necessárias

### Obtendo Ajuda

Se você encontrar problemas não listados aqui:

1. Verifique as [Issues](https://github.com/sus-data-explorer/sus-data-explorer/issues) existentes
2. Abra uma nova Issue descrevendo detalhadamente o problema
3. Entre em contato com a equipe de desenvolvimento através do e-mail suporte@susdataexplorer.org
