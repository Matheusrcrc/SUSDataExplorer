# 🔧 Como Adicionar o GitHub Actions Workflow

Devido a restrições de segurança do GitHub, o arquivo de workflow não pode ser adicionado automaticamente.
Siga os passos abaixo para configurar o deploy automático no GitHub Pages.

## Opção 1: Adicionar Manualmente via GitHub UI

1. Acesse seu repositório no GitHub
2. Vá em **Actions** → **New workflow**
3. Clique em **"set up a workflow yourself"**
4. Cole o conteúdo abaixo:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches:
      - main
      - master
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Pages
        uses: actions/configure-pages@v4

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: './docs'

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

5. Salve o arquivo como `.github/workflows/deploy-pages.yml`
6. Faça o commit

## Opção 2: Adicionar via Git Local

Se você tem permissões de push para workflows:

```bash
# Crie o diretório
mkdir -p .github/workflows

# Crie o arquivo
cat > .github/workflows/deploy-pages.yml << 'EOF'
name: Deploy to GitHub Pages

on:
  push:
    branches:
      - main
      - master
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Pages
        uses: actions/configure-pages@v4

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: './docs'

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
EOF

# Commit e push
git add .github/workflows/deploy-pages.yml
git commit -m "chore: Adicionar workflow do GitHub Actions para deploy no Pages"
git push
```

## Opção 3: Não Usar Workflow (Configuração Manual)

Você pode simplesmente habilitar o GitHub Pages sem workflow:

1. Vá em **Settings** → **Pages**
2. Em **Source**, selecione:
   - Branch: `main` (ou sua branch principal)
   - Folder: `/docs`
3. Clique em **Save**

O GitHub Pages irá publicar automaticamente os arquivos da pasta `docs/`.

**Nota**: Com esta opção, não haverá deploy automático via Actions, mas o conteúdo será servido normalmente.

## Verificar se Funcionou

Após configurar, verifique:

1. **Actions**: Vá em Actions no GitHub para ver os workflows rodando
2. **Settings → Pages**: Veja a URL do site publicado
3. Acesse a URL para confirmar que está funcionando

---

**Importante**: O workflow do GitHub Actions NÃO é obrigatório para usar o GitHub Pages.
A opção 3 (configuração manual) funciona perfeitamente e é mais simples!
