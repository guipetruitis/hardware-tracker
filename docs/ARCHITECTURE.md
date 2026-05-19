# Arquitetura do Projeto - Hardware Tracker

**Status:** Em Planejamento  
**Última Atualização:** 2026-05-18  
**Versão:** 0.1 (Draft)

---

## 1. Visão Geral da Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (React)                      │
│              (Responsivo: Mobile, Tablet, Web)          │
└────────────────────┬────────────────────────────────────┘
                     │ API REST / GraphQL
┌────────────────────▼────────────────────────────────────┐
│              Backend (Django + Python)                   │
│  ┌──────────────┬──────────────┬──────────────┐         │
│  │ Auth Service │ Core Service │ IA Service   │         │
│  └──────────────┴──────────────┴──────────────┘         │
└────────────────┬──────────────────────────────────────┘
                 │
    ┌────────────┼────────────┐
    │            │            │
    ▼            ▼            ▼
┌────────┐ ┌────────┐ ┌──────────┐
│PostgreSQL  │Cache    │Queue     │
│            │(Redis)  │(Celery)  │
└────────┘ └────────┘ └──────────┘
    │            │
    ▼            ▼
┌─────────────────────────────────────┐
│   Web Scraping (Selenium/BS4)      │
│   LLM APIs (Groq, Claude, Gemini)  │
│   n8n Workflows                    │
└─────────────────────────────────────┘
```

---

## 2. Componentes Principais

### 2.1 Frontend

**Framework:** React

**Responsabilidades:**
- Interface de usuário responsiva
- Modo claro/escuro
- Navegação e roteamento
- Integração com API Backend

**Bibliotecas Consideradas:**
- Tailwind CSS (estilos)
- React Router (roteamento)
- Axios/Fetch (requisições HTTP)
- Chart.js (gráficos de histórico de preços)

**Estrutura de Diretórios:**
```
frontend/
├── components/          # Componentes reutilizáveis
│   ├── Header
│   ├── Footer
│   ├── BuildCard
│   ├── PriceComparator
│   └── CompatibilityChecker
├── pages/              # Páginas principais
│   ├── Home
│   ├── Login
│   ├── BuildCreator
│   ├── Community
│   └── PieceDetails
├── services/           # Integração com API
│   └── api.js
├── hooks/              # Custom hooks
├── styles/             # CSS/Tailwind
└── assets/             # Imagens e ícones
```

### 2.2 Backend

**Framework:** Django + Django REST Framework (DRF)

**Responsabilidades:**
- APIs REST para Frontend
- Autenticação e autorização
- Lógica de negócio
- Integração com banco de dados
- Orquestração de scraping e LLM

**Apps Django Planejados:**
- `auth` — Autenticação de usuários
- `hardware` — Gestão de peças, comparador de preços
- `builds` — Criação e gerenciamento de builds
- `community` — Builds públicas, comentários, ranking
- `scraping` — Tasks de scraping de preços
- `ai_service` — Integração com LLMs, sugestões

**Estrutura de Diretórios:**
```
backend/
├── manage.py
├── requirements.txt
├── config/              # Configurações Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── auth/                # App de autenticação
├── hardware/            # App de hardware
├── builds/              # App de builds
├── community/           # App de comunidade
├── ai_service/          # App de IA
├── scraping/            # App de scraping
├── utils/               # Utilitários
└── tests/               # Testes
```

### 2.3 Banco de Dados

**SGBD:** PostgreSQL

**Entidades Principais:** (vide DATABASE.md)
- `User` — Usuários do sistema
- `Hardware` — Catálogo de peças
- `PriceHistory` — Histórico de preços
- `Build` — Builds criadas por usuários
- `Compatibility` — Regras de compatibilidade
- `Comment` — Comentários em builds

---

## 3. Padrões de Design

### 3.1 Backend

- **MVC (Model-View-Controller):** Django padrão
- **Repository Pattern:** Para acesso a dados (considerar)
- **Service Layer:** Lógica de negócio em services
- **Celery Tasks:** Para processamento assíncrono (scraping, LLM)

### 3.2 Frontend

- **Component-Based:** Componentes reutilizáveis
- **State Management:** Redux (ou Context API)
- **Custom Hooks:** Para lógica compartilhada
- **Responsive Design:** Mobile-first

---

## 4. Fluxo de Dados

### 4.1 Criação de Build

```
User Input (Frontend)
    ↓
API POST /builds/
    ↓
Django View: CreateBuildView
    ↓
Service: BuildService.create_build()
    ├─ Validate components
    ├─ Check compatibility
    └─ Save to DB
    ↓
Response JSON to Frontend
```

### 4.2 Scraping de Preços

```
Scheduled Task (Celery Beat)
    ↓
Celery Task: scrape_prices()
    ├─ For each store (Terabyte, Kabum, etc.)
    │   ├─ Selenium/BeautifulSoup scraping
    │   ├─ Parse HTML
    │   └─ Extract prices
    ├─ Store in Database
    └─ Update PriceHistory
    ↓
Frontend queries API GET /hardware/{id}/prices/history
```

### 4.3 Sugestões de IA

```
User Input: "Preciso de um PC gamer de R$ 3000"
    ↓
API POST /ai/suggest_build/
    ↓
Django View
    ├─ Query Reddit via RAG
    ├─ Call Groq/Claude LLM
    └─ Generate suggestions
    ↓
Format recommendations
    ↓
Response JSON with build suggestions
```

---

## 5. Decisões Técnicas

### 5.1 Frontend Framework

**Decisão:** React ✓

**Justificativa:** Maior peso em portfolio, ecossistema mais maduro para estado complexo (PC Builder, comparador de preços), e maior demanda de mercado no Brasil. Bibliotecas chave: React Query (caching de preços) e shadcn/ui (componentes).

### 5.2 State Management

**Decisão:** Zustand ✓

**Justificativa:** Estado complexo interligado no PC Builder (adicionar uma peça afeta compatibilidade, preço total e sugestões simultaneamente). Context API causaria re-renderizações na árvore inteira. Redux traz boilerplate excessivo para um projeto solo. Zustand oferece performance granular com API mínima.

### 5.3 Autenticação

**Decisão:** JWT ✓

**Justificativa:** Melhor adequação a APIs REST desacopladas (Django + React separados). Stateless, escalável horizontalmente e compatível com o Telegram bot via n8n.

### 5.4 Caching

**Decisão:** Duas camadas ✓

- **Redis (servidor):** Cache de preços scrapeados (TTL ~1h), regras de compatibilidade (TTL longo), rankings de builds. Já está no stack como broker do Celery — sem custo extra de infraestrutura.
- **React Query (cliente):** Cache automático de respostas da API no browser. Evita re-fetches desnecessários ao navegar entre páginas.
- **Cloudflare CDN:** Assets estáticos (imagens, JS, CSS). Já planejado no stack.

### 5.5 Task Queue

**Decisão:** Celery + Redis + n8n ✓

**Divisão de responsabilidades:**
- **Celery + Redis:** Processamento pesado e agendado — scraping de preços (Terabyte, Kabum, Amazon, Pichau) via Celery Beat, chamadas a LLMs (Groq, Claude, Gemini), workflows com dependências (`group` + `chord`).
- **n8n:** Automações visuais sem código — Bot de ofertas no Telegram, notificações de alertas de preço, webhooks de integração.

**Por que não Django-RQ:** Não tem agendador nativo, dependeria de cron externo — incompatível com arquitetura Docker.

---

## 6. Infraestrutura

### 6.1 Ambiente Local

- Docker Compose
  - Serviço Django
  - Serviço PostgreSQL
  - Serviço Redis
  - Serviço Celery Worker
  - Serviço Celery Beat (agendador)
  - Serviço n8n (automações: Telegram bot, notificações)
  - Serviço Frontend (Webpack Dev Server)

### 6.2 Produção

**Plataforma:** Render + Neon + Vercel (free tier para portfólio)

**Componentes:**
- **Backend (Django API):** Render — Web Service (free tier, dorme após inatividade)
- **Celery Worker:** Render — Background Worker
- **Redis:** Render — Redis (incluso no plano)
- **Database:** Neon — PostgreSQL serverless (free tier, escala a zero)
- **Frontend:** Vercel — React (free tier, CDN global)
- **DNS / CDN / SSL:** Cloudflare (gratuito)
- **Automações (n8n):** n8n Cloud free tier
- **CI/CD:** GitHub Actions

> **Limitação conhecida:** Render no free tier pausa o serviço após 15min de inatividade (cold start ~30s). Aceitável para portfólio; mitigar com um health check periódico via n8n ou UptimeRobot.

> **Plano de evolução:** Migrar para **Oracle Cloud Always Free** (4 vCPUs ARM + 24GB RAM) quando precisar de uptime contínuo ou querer demonstrar skills de DevOps com Docker Compose em VPS.

---

## 7. Segurança

- [ ] HTTPS obrigatório
- [ ] CSRF protection
- [ ] SQL Injection prevention (ORM)
- [ ] XSS prevention (Vue/React templating)
- [ ] Rate limiting nas APIs
- [ ] Validação de entrada
- [ ] Autenticação robusta (JWT + refresh tokens)
- [ ] Secrets management (variáveis de ambiente)

---

## 8. Performance

- [ ] Caching estratégico (Redis para preços)
- [ ] Database indexing
- [ ] Lazy loading de imagens
- [ ] Minificação de assets
- [ ] Gzip compression
- [ ] CDN para assets estáticos
- [ ] Paginação de resultados

---

## 9. Próximos Passos

1. [x] Decidir framework frontend → **React** ✓
2. [x] Definir state management → **Zustand** ✓
3. [x] Definir estratégia de cache → **Redis + React Query + Cloudflare** ✓
4. [x] Definir task queue → **Celery + Redis** (pesado) + **n8n** (Telegram/notificações) ✓
5. [ ] Criar wireframes no Figma
6. [ ] Definir modelo de dados detalhado
7. [ ] Desenhar diagramas de componentes
8. [ ] Planejar sprints de desenvolvimento
9. [ ] Configurar ambiente local (Docker Compose)

---

## 10. Referências

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Celery Documentation](https://docs.celeryproject.org/)
- [React Documentation](https://react.dev/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
