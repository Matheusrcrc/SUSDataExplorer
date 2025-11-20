# Driva by Matheus

**Plataforma B2B de Inteligência Comercial**

Aplicação web completa para mapear potencial de mercado, identificar oportunidades e automatizar cadências de prospecção multicanal com apoio de IA.

## 🚀 Funcionalidades

### ✅ Autenticação e Segurança
- Sistema de login seguro com NextAuth.js
- Controle de permissões por usuário (Admin, User, Viewer)
- Gerenciamento de organizações e equipes

### 🎯 Gestão de ICP (Cliente Ideal)
- Cadastro de perfis de clientes ideais via formulário
- Importação de ICPs via upload de planilhas (CSV, Excel)
- Segmentação por setor (CNAE), localização, porte e faturamento

### 🗺️ Mapeamento de Mercado
- Visualização em mapa/heatmap do potencial de mercado
- Filtros avançados por setor, região, faturamento e funcionários
- Estatísticas por região e setor

### 💾 Banco de Dados Setorizado
- Armazenamento estruturado de dados de empresas
- Filtros por CNAE, receita, região e outros critérios
- Dados enriquecidos automaticamente

### 📋 List Builder
- Filtragem avançada de leads
- Enriquecimento automático de dados (email, WhatsApp, LinkedIn)
- Exportação em CSV e Excel
- Importação de listas externas

### 📨 Workflow de Prospecção
- Automação de cadências multicanal:
  - Email
  - WhatsApp
  - LinkedIn
- Agendamento inteligente de contatos
- Sistema de notificações por evento
- Templates personalizáveis

### 🤖 IA Copilot
- Sugestões de abordagem personalizadas
- Geração de scripts para cada canal
- Recomendação de horários ideais para contato
- Análise de comportamento e performance

### 📊 Dashboard e Analytics
- KPIs em tempo real:
  - Total de leads
  - Campanhas ativas
  - ROI estimado
  - Taxa de conversão
- Funil de vendas visual
- Performance por canal
- Ranking de oportunidades
- Atividades recentes

### 👥 Multi-usuário e Colaboração
- Painel de administração
- Controle granular de permissões
- Trabalho colaborativo em tempo real
- Analytics de uso do aplicativo

## 🛠️ Stack Tecnológica

### Frontend
- **Next.js 14** (App Router) - Framework React
- **TypeScript** - Tipagem estática
- **Tailwind CSS** - Estilização utility-first
- **shadcn/ui** - Componentes UI modernos
- **Recharts** - Gráficos interativos
- **Leaflet/Mapbox** - Mapas e visualizações geográficas
- **React Hook Form + Zod** - Formulários e validação

### Backend
- **Next.js API Routes** - Backend serverless
- **PostgreSQL** - Banco de dados relacional
- **Prisma ORM** - Gerenciamento de dados type-safe
- **NextAuth.js** - Autenticação JWT

### Integrações
- **OpenAI/Anthropic** - IA Copilot
- **Node-cron** - Agendamento de tarefas
- **Nodemailer** - Envio de emails
- **APIs WhatsApp/LinkedIn** - Comunicação multicanal

## 📦 Instalação

### Pré-requisitos
- Node.js 18+
- PostgreSQL 14+
- npm ou yarn

### 1. Clone o repositório
```bash
git clone <repository-url>
cd driva-app
```

### 2. Instale as dependências
```bash
npm install
```

### 3. Configure as variáveis de ambiente
Copie o arquivo `.env.example` para `.env` e preencha as variáveis:

```bash
cp .env.example .env
```

Edite o arquivo `.env`:

```env
# Database
DATABASE_URL="postgresql://user:password@localhost:5432/driva_db"

# NextAuth
NEXTAUTH_URL="http://localhost:3000"
NEXTAUTH_SECRET="your-secret-key-here"

# OpenAI (para IA Copilot)
OPENAI_API_KEY="your-openai-api-key"

# Email (Nodemailer)
SMTP_HOST="smtp.gmail.com"
SMTP_PORT=587
SMTP_USER="your-email@gmail.com"
SMTP_PASS="your-app-password"

# WhatsApp API (exemplo: Twilio)
WHATSAPP_API_KEY="your-whatsapp-api-key"
WHATSAPP_PHONE_NUMBER="your-number"

# LinkedIn API
LINKEDIN_CLIENT_ID="your-linkedin-client-id"
LINKEDIN_CLIENT_SECRET="your-linkedin-client-secret"
```

### 4. Configure o banco de dados
```bash
# Gerar cliente Prisma
npm run prisma:generate

# Executar migrations
npm run prisma:migrate

# (Opcional) Abrir Prisma Studio para visualizar dados
npm run prisma:studio
```

### 5. Execute em modo desenvolvimento
```bash
npm run dev
```

Acesse: [http://localhost:3000](http://localhost:3000)

## 🏗️ Estrutura do Projeto

```
driva-app/
├── prisma/
│   └── schema.prisma          # Schema do banco de dados
├── public/                    # Arquivos estáticos
├── src/
│   ├── app/
│   │   ├── (auth)/
│   │   │   └── login/         # Página de login
│   │   ├── (dashboard)/       # Rotas protegidas
│   │   │   └── dashboard/
│   │   │       ├── icp/       # Gestão de ICP
│   │   │       ├── market-map/ # Mapeamento
│   │   │       ├── database/  # Banco de dados
│   │   │       ├── list-builder/ # List Builder
│   │   │       ├── prospecting/ # Prospecção
│   │   │       └── analytics/  # Analytics
│   │   ├── api/
│   │   │   ├── auth/          # Autenticação
│   │   │   ├── icp/           # APIs ICP
│   │   │   └── leads/         # APIs Leads
│   │   ├── layout.tsx         # Layout raiz
│   │   ├── page.tsx           # Página inicial
│   │   └── providers.tsx      # Providers (Session, Query)
│   ├── components/
│   │   ├── ui/                # Componentes UI base
│   │   └── dashboard/         # Componentes dashboard
│   ├── lib/
│   │   ├── auth.ts            # Configuração NextAuth
│   │   ├── prisma.ts          # Cliente Prisma
│   │   └── utils.ts           # Utilitários
│   └── types/                 # Tipos TypeScript
├── .env.example               # Exemplo de variáveis
├── next.config.js             # Configuração Next.js
├── package.json
├── tailwind.config.ts         # Configuração Tailwind
└── tsconfig.json              # Configuração TypeScript
```

## 📋 Schema do Banco de Dados

### Principais Modelos

- **User**: Usuários do sistema
- **Organization**: Organizações/empresas
- **ICPProfile**: Perfis de clientes ideais
- **Lead**: Leads/empresas prospectadas
- **ProspectingCampaign**: Campanhas de prospecção
- **CampaignLead**: Relação entre campanhas e leads
- **LeadInteraction**: Interações com leads
- **UserActivity**: Atividades dos usuários (analytics)
- **MarketData**: Dados de mercado para mapeamento

## 🚀 Deploy

### Build de Produção
```bash
npm run build
npm start
```

### Deploy na Vercel (Recomendado)
1. Conecte seu repositório na Vercel
2. Configure as variáveis de ambiente
3. Deploy automático!

### Outras Plataformas
- **Railway**: Suporta PostgreSQL + Next.js
- **Render**: Deploy fácil com banco de dados
- **AWS/Google Cloud**: Escalabilidade completa

## 🔑 Primeiro Acesso

Para criar o primeiro usuário admin, você pode usar o Prisma Studio:

```bash
npm run prisma:studio
```

Ou criar via script SQL direto no PostgreSQL.

## 📊 Roadmap Futuro

- [ ] Integração com APIs de dados empresariais (Serasa, CNPJ.ws)
- [ ] Implementação completa de mapa interativo (Leaflet/Mapbox)
- [ ] Sistema de notificações em tempo real (WebSockets)
- [ ] App mobile (React Native)
- [ ] Integração com CRMs (Salesforce, HubSpot, Pipedrive)
- [ ] IA para scoring automático de leads
- [ ] Relatórios avançados em PDF
- [ ] Webhooks para integrações externas

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob licença proprietária. Todos os direitos reservados.

## 👨‍💻 Autor

**Matheus**

---

**Driva by Matheus** - Transformando dados em oportunidades de negócio 🚀
