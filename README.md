# Hardware Tracker

Plataforma brasileira de montagem de PCs e comparação de preços, inspirada no [meupc.net](https://meupc.net/).

Monitoramento de preços em tempo real nas principais lojas (KaBuM!, Pichau, Terabyte, Amazon), verificador de compatibilidade entre componentes e ferramenta de build com IA integrada.

> **Status:** Em desenvolvimento — Sprint 0 (Setup & Modelagem)

---

## Stack

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Django](https://img.shields.io/badge/Django-5.x-green?logo=django)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue?logo=postgresql)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker)

| Camada | Tecnologia |
|--------|-----------|
| Backend | Python 3.12 + Django 5 + Django REST Framework |
| Frontend | React 18 + TypeScript + Tailwind CSS |
| Banco de Dados | PostgreSQL 16 (JSONB para specs de hardware) |
| Scraping | Python (Playwright / BeautifulSoup) |
| Orquestração | Celery + Redis / n8n |
| IA | Groq SDK / Claude API / RAG com pgvector |
| Infra | Docker Compose (local) · AWS + Cloudflare (produção) |

---

## Funcionalidades

- **Comparador de Preços** — agrega preços de KaBuM!, Pichau, Terabyte e Amazon com histórico gráfico
- **PC Builder** — montagem de build com verificação de compatibilidade em tempo real
- **IA Integrada** — sugestões de peças por orçamento/uso e avaliação da build
- **Alertas de Preço** — notificação via Telegram quando a peça atingir o preço-alvo *(Post-MVP)*

---

## Como rodar localmente

> **Pré-requisitos:** Docker e Docker Compose instalados.

```bash
# Clone o repositório
git clone https://github.com/guipetruitis/hardware-tracker.git
cd hardware-tracker

# Copie as variáveis de ambiente
cp .env.example .env

# Suba os containers
docker compose up --build
```

| Serviço | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend (API) | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |
| pgAdmin | http://localhost:5050 |

> **Nota:** O `docker-compose.yml` e as aplicações ainda estão em construção (Sprint 0).

---

## Documentação

| Arquivo | Conteúdo |
|---------|---------|
| [docs/REQUIREMENTS.md](docs/REQUIREMENTS.md) | Levantamento de requisitos e User Stories |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Decisões arquiteturais e stack técnico |
| [docs/DATABASE.md](docs/DATABASE.md) | Modelagem do banco de dados (ER + DDL) |
| [docs/TESTING.md](docs/TESTING.md) | Estratégia de testes |

---

## Estrutura do Projeto

```
hardware-tracker/
├── backend/          # API Django + DRF
├── frontend/         # React + TypeScript
├── docs/             # Documentação técnica
├── design/           # Wireframes e protótipos
├── .github/          # CI/CD (GitHub Actions)
└── docker-compose.yml
```

---

## Licença

MIT
