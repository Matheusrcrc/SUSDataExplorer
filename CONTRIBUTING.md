# Contribuindo para o SUS Data Explorer

Obrigado pelo seu interesse em contribuir para o SUS Data Explorer! Este guia ajudará você a entender como pode participar do desenvolvimento deste projeto open source.

## Código de Conduta

Ao participar deste projeto, você concorda em seguir nosso [Código de Conduta](CODE_OF_CONDUCT.md). Por favor, leia-o antes de contribuir.

## Como Contribuir

Existem várias maneiras de contribuir para o SUS Data Explorer:

### 1. Reportando Bugs

Se você encontrar um bug, por favor, abra uma issue usando o template de bug report. Inclua:

- Uma descrição clara do problema
- Passos para reproduzir o bug
- Comportamento esperado vs. comportamento observado
- Capturas de tela, se aplicável
- Informações sobre seu ambiente (sistema operacional, versão do Python, etc.)

### 2. Sugerindo Melhorias

Para sugerir melhorias ou novos recursos, abra uma issue usando o template de feature request. Descreva:

- O que você gostaria de ver implementado
- Por que isso seria útil para o projeto
- Como você imagina que isso funcionaria

### 3. Solicitando Novos Datasets

Se você precisa de acesso a um dataset específico do SUS que ainda não está disponível no projeto, abra uma issue usando o template de dataset-request. Inclua:

- Nome e descrição do dataset
- Fonte oficial do dataset (URL)
- Justificativa para inclusão
- Exemplos de uso potencial

### 4. Contribuindo com Código

Para contribuir com código:

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nome-da-feature`)
3. Implemente suas mudanças
4. Adicione testes para suas mudanças
5. Execute os testes para garantir que tudo está funcionando
6. Faça commit das suas mudanças (`git commit -m 'Adiciona nova feature'`)
7. Envie para o GitHub (`git push origin feature/nome-da-feature`)
8. Abra um Pull Request

#### Diretrizes de Código

- Siga as convenções de estilo PEP 8 para Python
- Escreva testes para novas funcionalidades
- Mantenha a cobertura de testes acima de 90%
- Documente seu código usando docstrings
- Atualize a documentação quando necessário

### 5. Melhorando a Documentação

A documentação é crucial para o sucesso do projeto. Você pode ajudar:

- Corrigindo erros de ortografia ou gramática
- Melhorando explicações existentes
- Adicionando exemplos de uso
- Criando tutoriais ou guias

## Processo de Desenvolvimento

### Fluxo de Trabalho

1. As issues são triadas e priorizadas pela equipe principal
2. As issues são atribuídas a colaboradores ou ficam disponíveis para quem quiser trabalhar nelas
3. O trabalho é realizado em branches separadas
4. Pull Requests são revisados pela equipe principal
5. Após aprovação, o código é mesclado à branch principal

### Convenções de Commit

Usamos mensagens de commit semânticas:

- `feat:` para novas funcionalidades
- `fix:` para correções de bugs
- `docs:` para mudanças na documentação
- `style:` para formatação de código
- `refactor:` para refatorações de código
- `test:` para adição ou modificação de testes
- `chore:` para tarefas de manutenção

Exemplo: `feat: adiciona suporte para exportação em formato Excel`

## Ambiente de Desenvolvimento

### Requisitos

- Python 3.10 ou superior
- Poetry para gerenciamento de dependências

### Configuração

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/sus-data-explorer.git
cd sus-data-explorer

# Instale as dependências com Poetry
poetry install

# Ative o ambiente virtual
poetry shell

# Execute os testes
pytest
```

## Estrutura do Projeto

```
sus-data-explorer/
├── connectors/       # Conectores para fontes de dados
├── api/              # API FastAPI e CLI
├── mobile/           # Aplicativo mobile
├── notebooks/        # Notebooks de análise
├── tests/            # Testes automatizados
└── docs/             # Documentação
```

## Licença

Ao contribuir para este projeto, você concorda que suas contribuições serão licenciadas sob a mesma licença do projeto (MIT).

## Perguntas?

Se você tiver dúvidas sobre como contribuir, sinta-se à vontade para abrir uma issue com a tag "question".

Agradecemos sua contribuição para tornar o acesso aos dados do SUS mais fácil e eficiente!
