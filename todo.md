# SUS Data Explorer - Lista de Tarefas

## Análise do Documento do Projeto
- [x] Ler e compreender o documento do projeto
- [x] Identificar requisitos e escopo
- [x] Confirmar detalhes com o usuário

## Configuração do Ambiente de Desenvolvimento
- [x] Criar repositório Git
- [x] Inicializar Poetry para gerenciamento de dependências
- [ ] Configurar CI básico
- [ ] Gerar README com diagrama C4 e TOC
- [x] Instalar dependências necessárias (Python 3.10, FastAPI, etc.)

## Implementação dos Data Connectors
- [x] Implementar connector para CKAN OpenDataSUS
- [x] Implementar connector para DEMAS / apidadosabertos.saude.gov.br
- [x] Implementar connector para DATASUS TABNET via PySUS
- [x] Implementar connector para e-Gestor AB (scraping)
- [x] Documentar variáveis, políticas de atualização e limitações

## Desenvolvimento da Core API & CLI
- [x] Criar endpoints `/indicators/{code}` e `/exports`
- [x] Desenvolver CLI `susx pull <fonte> --region 290001 --years 2013:2023`
- [ ] Implementar cache com Redis
- [ ] Garantir idempotência e logs estruturados (OpenTelemetry)

## Criação do MVP Mobile
- [x] Implementar autenticação GitHub/OAuth
- [x] Desenvolver dashboards com ECharts/Plotly
- [x] Criar interface responsiva
- [x] Implementar funcionalidade de drill-down

## Implementação da Pesquisa IAM-Bahia
- [x] Criar scripts de parâmetros reproduzíveis
- [x] Desenvolver notebook `iam_bahia.ipynb`
- [ ] Implementar visualizações específicas para a pesquisa

## Configuração de Governança e Comunidade
- [x] Criar Wiki "Como contribuir"
- [x] Desenvolver templates para Issues
- [x] Automatizar publicação de releases
- [x] Configurar documentação em ReadTheDocs

## Testes e Validação
- [x] Implementar testes unitários com pytest
- [x] Garantir cobertura de testes >90%
- [x] Realizar testes de contrato nos conectores
- [x] Validar desempenho (respostas <300ms em cache quente)

## Documentação e Entrega
- [x] Finalizar documentação do código
- [x] Criar documentação de uso
- [x] Preparar formatos de saída apresentáveis (site, PDF, XLS)
- [x] Entregar projeto completo
