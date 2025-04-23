# SUS Data Explorer - Documentação Técnica

## Visão Geral da Arquitetura

O SUS Data Explorer é um sistema distribuído com arquitetura modular, projetado para buscar, unificar e servir dados oficiais do SUS. Esta documentação técnica fornece detalhes sobre a arquitetura, componentes e fluxos de dados do sistema.

## Índice

1. [Arquitetura do Sistema](#arquitetura-do-sistema)
2. [Conectores de Dados](#conectores-de-dados)
3. [API Core](#api-core)
4. [Interface de Linha de Comando](#interface-de-linha-de-comando)
5. [Aplicativo Mobile](#aplicativo-mobile)
6. [Fluxo de Dados](#fluxo-de-dados)
7. [Segurança](#segurança)
8. [Escalabilidade](#escalabilidade)
9. [Monitoramento](#monitoramento)

## Arquitetura do Sistema

O SUS Data Explorer segue uma arquitetura de microserviços, com os seguintes componentes principais:

```
+-------------------+     +-------------------+     +-------------------+
|                   |     |                   |     |                   |
|  Fontes de Dados  |     |  Conectores       |     |  API Core         |
|  do SUS           +---->+  de Dados         +---->+  (FastAPI)        |
|                   |     |                   |     |                   |
+-------------------+     +-------------------+     +--------+----------+
                                                             |
                                                             v
                          +-------------------+     +-------------------+
                          |                   |     |                   |
                          |  CLI              |<----+  Camada de        |
                          |  (Typer)          |     |  Serviços         |
                          |                   |     |                   |
                          +-------------------+     +--------+----------+
                                                             |
                                                             v
                                                    +-------------------+
                                                    |                   |
                                                    |  Aplicativo       |
                                                    |  Mobile           |
                                                    |  (React Native)   |
                                                    |                   |
                                                    +-------------------+
```

### Princípios de Design

- **AI First**: Utilização de técnicas de IA para melhorar a busca, normalização e análise de dados
- **Mobile First**: Design responsivo e otimizado para dispositivos móveis
- **Community First**: Código aberto e documentação abrangente para facilitar contribuições
- **Local First**: Suporte a operações offline e sincronização posterior

## Conectores de Dados

Os conectores de dados são responsáveis por acessar diferentes fontes de dados do SUS, normalizar os dados e disponibilizá-los em um formato padronizado.

### Hierarquia de Classes

```
                  +-------------------+
                  |                   |
                  |  DataConnector    |
                  |  (Classe Base)    |
                  |                   |
                  +--------+----------+
                           |
           +---------------+---------------+---------------+
           |               |               |               |
+----------v----+  +-------v-------+  +----v---------+  +-v-------------+
|               |  |               |  |              |  |               |
| CkanConnector |  | DemasConnector|  |TabnetConnector|  |EGestorConnector|
|               |  |               |  |              |  |               |
+---------------+  +---------------+  +--------------+  +---------------+
```

### Interface Comum

Todos os conectores implementam a seguinte interface:

- `list_datasets()`: Lista os datasets disponíveis
- `fetch(query)`: Busca dados brutos da fonte
- `normalize(data)`: Normaliza os dados em um DataFrame pandas
- `schema()`: Retorna o schema do conector
- `get_data(query)`: Método de conveniência que combina fetch() e normalize()

### Detalhes dos Conectores

#### CkanConnector

- **Fonte**: OpenDataSUS (CKAN)
- **Protocolo**: API REST
- **Formato de Dados**: JSON
- **Autenticação**: Não requerida

#### DemasConnector

- **Fonte**: DEMAS (Departamento de Monitoramento e Avaliação do SUS)
- **Protocolo**: API REST
- **Formato de Dados**: JSON
- **Autenticação**: Não requerida

#### TabnetConnector

- **Fonte**: DATASUS TABNET
- **Protocolo**: Biblioteca PySUS
- **Formato de Dados**: DBF/CSV
- **Autenticação**: Não requerida

#### EGestorConnector

- **Fonte**: e-Gestor AB
- **Protocolo**: Web Scraping
- **Formato de Dados**: HTML/CSV
- **Autenticação**: Requerida (em alguns casos)

## API Core

A API Core é implementada usando FastAPI e fornece endpoints RESTful para acessar os dados do SUS.

### Endpoints Principais

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/` | GET | Informações sobre a API |
| `/sources` | GET | Lista todas as fontes de dados |
| `/datasets` | GET | Lista todos os datasets |
| `/datasets/{source}` | GET | Lista datasets de uma fonte específica |
| `/indicators/{code}` | GET | Obtém dados de um indicador |
| `/exports` | GET | Exporta dados em diferentes formatos |

### Modelos de Dados

- `Source`: Representa uma fonte de dados
- `Dataset`: Representa um dataset
- `IndicatorResponse`: Representa a resposta de um indicador
- `ExportResponse`: Representa a resposta de uma exportação

### Middleware

- CORS: Permite acesso de diferentes origens
- Logging: Registra todas as requisições e respostas
- Error Handling: Tratamento centralizado de erros

## Interface de Linha de Comando

A CLI é implementada usando Typer e fornece comandos para acessar os dados do SUS via terminal.

### Comandos Principais

| Comando | Descrição |
|---------|-----------|
| `list-sources` | Lista todas as fontes de dados |
| `list-datasets` | Lista todos os datasets |
| `pull-data` | Obtém dados e salva em arquivo |
| `info` | Exibe informações sobre o sistema |

### Fluxo de Execução

1. Parsing de argumentos
2. Validação de parâmetros
3. Execução assíncrona de operações
4. Formatação e exibição de resultados

## Aplicativo Mobile

O aplicativo mobile é implementado usando React Native e fornece uma interface gráfica para acessar os dados do SUS.

### Componentes Principais

- `AuthScreen`: Tela de autenticação
- `DashboardScreen`: Tela principal com visualizações
- `DatasetScreen`: Tela de detalhes de dataset
- `SettingsScreen`: Tela de configurações

### Estado da Aplicação

- Redux para gerenciamento de estado global
- AsyncStorage para persistência local
- Context API para estados específicos de componentes

### Navegação

- React Navigation para gerenciamento de rotas
- Drawer Navigator para menu lateral
- Stack Navigator para navegação entre telas

## Fluxo de Dados

### Fluxo de Busca de Dados

1. Usuário solicita dados via API, CLI ou aplicativo mobile
2. A solicitação é roteada para o conector apropriado
3. O conector busca os dados da fonte original
4. Os dados são normalizados em um formato padronizado
5. Os dados são retornados ao usuário

### Fluxo de Exportação

1. Usuário solicita exportação de dados
2. Os dados são obtidos via fluxo de busca
3. Os dados são convertidos para o formato solicitado
4. O arquivo é gerado e disponibilizado para download

### Fluxo de Autenticação

1. Usuário inicia processo de autenticação
2. Usuário é redirecionado para provedor OAuth (GitHub)
3. Após autenticação, o usuário é redirecionado de volta
4. Token de acesso é gerado e armazenado
5. Token é usado para autenticar requisições subsequentes

## Segurança

### Autenticação

- OAuth 2.0 para autenticação de usuários
- Tokens JWT para sessões
- Refresh tokens para renovação automática

### Autorização

- RBAC (Role-Based Access Control) para controle de acesso
- Middleware de autorização para validação de permissões

### Proteção de Dados

- HTTPS para comunicação segura
- Sanitização de inputs para prevenir injeções
- Rate limiting para prevenir abusos

## Escalabilidade

### Estratégias de Escalabilidade

- Arquitetura stateless para facilitar escalabilidade horizontal
- Caching de resultados frequentes
- Processamento assíncrono para operações longas

### Otimizações

- Conexões HTTP persistentes
- Pooling de conexões de banco de dados
- Compressão de respostas

## Monitoramento

### Métricas Coletadas

- Tempo de resposta de endpoints
- Taxa de erros
- Uso de recursos (CPU, memória)
- Número de requisições por endpoint

### Logging

- Logs estruturados em formato JSON
- Níveis de log configuráveis
- Rotação de logs automática

### Alertas

- Alertas para erros críticos
- Alertas para degradação de performance
- Alertas para indisponibilidade de fontes de dados
