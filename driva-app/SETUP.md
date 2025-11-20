# Guia de Setup Rápido - Driva by Matheus

## 🚀 Início Rápido (5 minutos)

### 1. Instalar Dependências
```bash
cd driva-app
npm install
```

### 2. Configurar Banco de Dados Local

#### Opção A: PostgreSQL Local
```bash
# Instalar PostgreSQL (Ubuntu/Debian)
sudo apt-get install postgresql postgresql-contrib

# Criar banco de dados
sudo -u postgres createdb driva_db

# Criar usuário
sudo -u postgres psql
postgres=# CREATE USER driva_user WITH PASSWORD 'sua_senha';
postgres=# GRANT ALL PRIVILEGES ON DATABASE driva_db TO driva_user;
postgres=# \q
```

#### Opção B: Docker (Recomendado para Desenvolvimento)
```bash
# Criar container PostgreSQL
docker run --name driva-postgres \
  -e POSTGRES_PASSWORD=driva123 \
  -e POSTGRES_USER=driva_user \
  -e POSTGRES_DB=driva_db \
  -p 5432:5432 \
  -d postgres:14

# Verificar se está rodando
docker ps
```

### 3. Configurar Variáveis de Ambiente
```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar .env com suas configurações
nano .env  # ou use seu editor preferido
```

**Configuração Mínima para Começar:**
```env
DATABASE_URL="postgresql://driva_user:driva123@localhost:5432/driva_db"
NEXTAUTH_URL="http://localhost:3000"
NEXTAUTH_SECRET="desenvolvimento-secret-key-change-in-production"
```

### 4. Inicializar Banco de Dados
```bash
# Gerar cliente Prisma
npm run prisma:generate

# Criar tabelas
npm run prisma:migrate

# (Opcional) Visualizar dados
npm run prisma:studio
```

### 5. Executar Aplicação
```bash
npm run dev
```

Acesse: **http://localhost:3000**

---

## 📝 Criar Primeiro Usuário

Você precisa criar manualmente o primeiro usuário admin. Use uma destas opções:

### Opção 1: Prisma Studio (Mais Fácil)
```bash
npm run prisma:studio
```
1. Abra http://localhost:5555
2. Clique em "User"
3. Clique em "Add record"
4. Preencha:
   - email: `admin@driva.com`
   - name: `Admin`
   - password: Use um hash bcrypt (veja abaixo)
   - role: `ADMIN`
5. Salve

### Opção 2: Script Node.js
Crie um arquivo `scripts/create-admin.js`:
```javascript
const { PrismaClient } = require('@prisma/client');
const bcrypt = require('bcryptjs');

const prisma = new PrismaClient();

async function main() {
  const hashedPassword = await bcrypt.hash('admin123', 10);

  const admin = await prisma.user.create({
    data: {
      email: 'admin@driva.com',
      name: 'Admin',
      password: hashedPassword,
      role: 'ADMIN',
    },
  });

  console.log('Admin criado:', admin);
}

main()
  .catch(console.error)
  .finally(() => prisma.$disconnect());
```

Execute:
```bash
node scripts/create-admin.js
```

### Gerar Hash de Senha (Bcrypt)
```javascript
// No Node.js console ou arquivo
const bcrypt = require('bcryptjs');
const hash = bcrypt.hashSync('sua_senha', 10);
console.log(hash);
```

---

## 🔧 Configurações Opcionais

### IA Copilot (OpenAI)
```env
OPENAI_API_KEY="sk-..."
```

### Email (Gmail exemplo)
```env
SMTP_HOST="smtp.gmail.com"
SMTP_PORT=587
SMTP_USER="seu@gmail.com"
SMTP_PASS="sua_senha_app"  # Use senha de app, não a senha normal
```

**Como gerar senha de app no Gmail:**
1. Acesse: https://myaccount.google.com/apppasswords
2. Gere uma senha para "Mail"
3. Use essa senha no `.env`

### WhatsApp (Twilio exemplo)
```env
WHATSAPP_API_KEY="seu_auth_token"
WHATSAPP_PHONE_NUMBER="+5511999999999"
```

### LinkedIn API
```env
LINKEDIN_CLIENT_ID="seu_client_id"
LINKEDIN_CLIENT_SECRET="seu_client_secret"
```

---

## 🐛 Troubleshooting

### Erro: "Can't connect to database"
- Verifique se o PostgreSQL está rodando
- Confirme a `DATABASE_URL` no `.env`
- Teste a conexão: `psql -h localhost -U driva_user -d driva_db`

### Erro: "Prisma Client not found"
```bash
npm run prisma:generate
```

### Erro: "Module not found"
```bash
rm -rf node_modules package-lock.json
npm install
```

### Porta 3000 já em uso
```bash
# Linux/Mac
lsof -ti:3000 | xargs kill -9

# Ou mude a porta
PORT=3001 npm run dev
```

---

## 📚 Próximos Passos

1. ✅ Faça login com o usuário admin
2. ✅ Crie seu primeiro ICP
3. ✅ Importe uma lista de leads (CSV)
4. ✅ Configure uma campanha de prospecção
5. ✅ Explore o dashboard e analytics

---

## 🆘 Suporte

Para dúvidas ou problemas:
- Consulte o [README.md](./README.md)
- Verifique os logs do terminal
- Abra uma issue no repositório

---

**Bom trabalho! 🚀**
