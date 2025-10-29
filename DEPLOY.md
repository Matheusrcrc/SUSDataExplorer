# 🚀 Guia de Deploy - SUS Data Explorer

Este guia explica como fazer o deploy do SUS Data Explorer usando Streamlit Cloud (gratuito) e GitHub Pages.

## 📋 Índice

1. [Deploy no Streamlit Cloud](#deploy-no-streamlit-cloud)
2. [Deploy no GitHub Pages](#deploy-no-github-pages)
3. [Executar Localmente](#executar-localmente)
4. [Troubleshooting](#troubleshooting)

---

## 🎈 Deploy no Streamlit Cloud

O Streamlit Cloud oferece hospedagem gratuita para aplicações Streamlit diretamente do GitHub.

### Pré-requisitos

- Conta no GitHub
- Repositório público ou privado no GitHub
- Conta no [Streamlit Cloud](https://streamlit.io/cloud) (gratuita)

### Passo a Passo

#### 1. Preparar o Repositório

Certifique-se de que seu repositório contém:

```
SUSDataExplorer/
├── app_streamlit.py         # Aplicação principal
├── requirements.txt         # Dependências Python
├── packages.txt            # Dependências do sistema (opcional)
├── .streamlit/
│   ├── config.toml         # Configurações do Streamlit
│   └── secrets.toml.example # Exemplo de secrets
├── ckan.py                 # Conectores
├── demas.py
├── tabnet.py
└── egestor.py
```

#### 2. Fazer Push para o GitHub

```bash
git add .
git commit -m "Deploy: Preparar aplicação Streamlit"
git push origin main
```

#### 3. Configurar no Streamlit Cloud

1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Clique em **"New app"**
3. Selecione seu repositório: `seu-usuario/SUSDataExplorer`
4. Branch: `main` (ou a branch desejada)
5. Main file path: `app_streamlit.py`
6. Clique em **"Deploy!"**

#### 4. Configurar Secrets (Opcional)

Se sua aplicação precisar de secrets (API keys, etc.):

1. No painel do Streamlit Cloud, vá em **Settings** → **Secrets**
2. Adicione os secrets no formato TOML:

```toml
# Exemplo
[cache]
ttl = 3600
```

#### 5. Acessar a Aplicação

Após alguns minutos, sua aplicação estará disponível em:
```
https://seu-usuario-susdataexplorer-app-streamlit-xxxxx.streamlit.app
```

### Atualizações Automáticas

O Streamlit Cloud sincroniza automaticamente com seu repositório. Cada push para a branch configurada irá:

1. Detectar as mudanças
2. Reinstalar dependências (se necessário)
3. Reiniciar a aplicação

---

## 🌐 Deploy no GitHub Pages

GitHub Pages oferece hospedagem gratuita para sites estáticos (landing page).

### Pré-requisitos

- Repositório público no GitHub
- Arquivos HTML na pasta `docs/`

### Passo a Passo

#### 1. Verificar Arquivos

Certifique-se de que a pasta `docs/` contém:

```
docs/
└── index.html    # Página principal
```

#### 2. Habilitar GitHub Pages

1. Acesse seu repositório no GitHub
2. Vá em **Settings** → **Pages**
3. Em **Source**, selecione:
   - Branch: `main`
   - Folder: `/docs`
4. Clique em **Save**

#### 3. GitHub Actions (Automático)

O workflow já está configurado em `.github/workflows/deploy-pages.yml`.

Cada push para `main` irá:
- Pegar os arquivos da pasta `docs/`
- Fazer deploy automático no GitHub Pages

#### 4. Acessar o Site

Após alguns minutos, seu site estará disponível em:
```
https://seu-usuario.github.io/SUSDataExplorer
```

#### 5. Atualizar Link do Streamlit

Edite `docs/index.html` e atualize a URL do Streamlit:

```javascript
// Linha ~458
const streamlitUrl = 'https://seu-usuario-susdataexplorer-app-streamlit-xxxxx.streamlit.app';
```

---

## 💻 Executar Localmente

### Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/SUSDataExplorer.git
cd SUSDataExplorer

# 2. Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt
```

### Executar a Aplicação Streamlit

```bash
streamlit run app_streamlit.py
```

A aplicação estará disponível em: `http://localhost:8501`

### Executar Testes

```bash
# Executar todos os testes
pytest

# Com cobertura
pytest --cov

# Apenas testes específicos
pytest test_connectors.py
```

---

## 🔧 Troubleshooting

### Problema: Erro ao importar conectores

**Erro:**
```
ModuleNotFoundError: No module named 'ckan'
```

**Solução:**
Certifique-se de que todos os arquivos de conectores estão no mesmo diretório que `app_streamlit.py`:
```
SUSDataExplorer/
├── app_streamlit.py
├── ckan.py
├── demas.py
├── tabnet.py
└── egestor.py
```

### Problema: Dependências faltando no Streamlit Cloud

**Erro:**
```
ModuleNotFoundError: No module named 'plotly'
```

**Solução:**
Verifique se `requirements.txt` contém todas as dependências:
```txt
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.17.0
```

### Problema: GitHub Pages não atualiza

**Solução:**
1. Verifique se o workflow foi executado: **Actions** → **Deploy to GitHub Pages**
2. Limpe o cache do navegador (Ctrl+Shift+R)
3. Aguarde alguns minutos para propagação

### Problema: Aplicação Streamlit lenta

**Solução:**
1. Verifique o cache:
```python
@st.cache_data(ttl=3600)  # Cache por 1 hora
def load_data():
    ...
```

2. Reduza o tamanho dos dados:
```python
# Limite o número de registros
data = data.head(10000)
```

### Problema: Erro de timeout em requisições

**Solução:**
Aumente o timeout dos conectores:
```python
self.client = httpx.AsyncClient(timeout=60.0)  # 60 segundos
```

---

## 🔐 Segurança

### Secrets e API Keys

**NUNCA** commit secrets ou API keys no repositório!

1. Use `.env` local (já está no `.gitignore`):
```bash
# .env
API_KEY=sua_chave_secreta
```

2. Use Streamlit Secrets para produção:
```toml
# .streamlit/secrets.toml (não commitado)
api_key = "sua_chave_secreta"
```

3. Acesse no código:
```python
import streamlit as st
api_key = st.secrets["api_key"]
```

---

## 🌟 Recursos Adicionais

- [Documentação Streamlit](https://docs.streamlit.io)
- [GitHub Pages Docs](https://docs.github.com/pages)
- [GitHub Actions](https://docs.github.com/actions)

---

## 🎯 Próximos Passos

Após o deploy, você pode:

1. ✅ Adicionar domínio customizado
2. ✅ Configurar analytics
3. ✅ Adicionar autenticação
4. ✅ Implementar cache Redis
5. ✅ Monitoramento com logs

---

**Feito com ❤️ para o SUS Data Explorer**
