# Roadmap — Hardware Tracker

**Última Atualização:** 2026-06-03
**Branch atual:** develop

---

## Estado Atual

| Artefato | Status |
|----------|--------|
| Scaffold Django + estrutura de pastas | ✅ Feito |
| Modelagem do BD (DATABASE.md) | ✅ Feito |
| Arquitetura definida (ARCHITECTURE.md) | ✅ Feito |
| CI/CD básico (.github/workflows) | ✅ Feito |
| Implementação do backend | 🔲 Pendente |
| Frontend | 🔲 Pendente |
| Scraping | 🔲 Pendente |

---

## Bloco 1 — Backend: Estrutura Django

> Prioridade: **Alta** — bloqueadores devem ser resolvidos antes de qualquer migration.

- [ ] Adicionar `AUTH_USER_MODEL` em `settings.py` (**bloqueador crítico**)
- [ ] Criar os apps Django: `users`, `hardware`, `builds`, `community`, `alerts`, `scraping`
- [ ] Implementar `models.py` por app (baseado em DATABASE.md)
- [ ] Criar e rodar migrations em ambiente local (Docker + PostgreSQL)
- [ ] Criar fixtures de seed: categorias, lojas (Terabyte, KaBuM!, Amazon, Pichau) e hardwares populares

---

## Bloco 2 — Backend: API REST

> Prioridade: **Média** — depende do Bloco 1.

- [ ] Configurar Django REST Framework e serializers por app
- [ ] Endpoints base: hardware (listagem, detalhe), builds (CRUD), prices (comparador)
- [ ] Autenticação: registro, login, JWT com cookies `HttpOnly`

---

## Bloco 3 — Infra / DevOps

> Prioridade: **Média** — pode ser feito em paralelo ao Bloco 1.

- [ ] Entender o CI/CD do zero — estudar o `ci.yml` scaffoldado (sessão dedicada)
- [ ] Configurar Docker Compose local: PostgreSQL + Redis + Django

---

## Bloco 4 — Frontend

> Prioridade: **Baixa** — depende da API estar funcional.

- [ ] Setup React com Vite + Tailwind + React Router
- [ ] Páginas base: Home, Login, Catálogo de Hardware
- [ ] Integração com a API Django

---

## Bloco 5 — Scraping

> Prioridade: **Baixa** — depende dos models de `hardware`, `prices` e `price_history`.

- [ ] Scraper MVP: Terabyte + KaBuM! com BeautifulSoup/Selenium
- [ ] Celery + Celery Beat: job diário às 03:00 BRT
- [ ] Persistir dados em `prices` e `price_history`

---

## Referências

- [DATABASE.md](DATABASE.md) — Modelagem do banco de dados
- [ARCHITECTURE.md](ARCHITECTURE.md) — Decisões arquiteturais
- [REQUIREMENTS.md](REQUIREMENTS.md) — Levantamento de requisitos
- [TESTING.md](TESTING.md) — Estratégia de testes
