# Roadmap — Hardware Tracker

**Última Atualização:** 2026-07-07
**Branch atual:** feat/hardware-models

> Cada sessão listada abaixo corresponde a uma branch (`feat/`, `fix/`, `chore/`) com PR próprio para `develop`, seguindo o fluxo de git do projeto. A ordem é sugerida por dependência técnica, não é obrigatória — reavaliar prioridade a cada sessão.

---

## Estado Atual

| Área | Status |
|---|---|
| Scaffold Django (6 apps: users, hardware, builds, community, alerts, scraping) | ✅ Feito |
| Model `User` customizado + `AUTH_USER_MODEL` | ✅ Feito |
| Docker + docker-compose (dev local) | ✅ Feito |
| CI básico (GitHub Actions: checkout@v5, setup-python@v6, flake8) | ✅ Feito |
| Documentação (REQUIREMENTS, ARCHITECTURE, DATABASE, TESTING, SECURITY_AUDIT) | ✅ Feito |
| Models do app `hardware` (Category, Hardware, Store, Price, PriceHistory) | 🔶 Em andamento — não commitado, ver pendências da Sessão 1 |
| `admin.py` do app `hardware` | 🔲 Pendente |
| Models de `builds`, `community`, `alerts`, `scraping` (Coupon) | 🔲 Pendente — stubs vazios |
| Correções do Security Audit 2026-06-03 (8 itens) | 🔲 Pendente — bloqueador antes de deploy/frontend |
| API REST (DRF) | 🔲 Não iniciado |
| Autenticação (JWT) | 🔲 Não iniciado |
| Testes automatizados (pytest) | 🔲 Não iniciado |
| Scraping | 🔲 Não iniciado |
| Frontend | 🔲 Não iniciado |
| IA / RAG (Post-MVP) | 🔲 Não iniciado |

---

## Fase 1 — Fechar a Modelagem do Banco

### Sessão 1 (atual): `feat/hardware-models`

**Contexto:** já existem models não commitados de Category, Hardware, Store, Price e PriceHistory.

- [ ] Rodar `python manage.py check` antes de seguir — há pelo menos dois problemas a investigar:
  - indentação do docstring da classe `Store`
  - `Price.__str__` referencia um campo que não existe no model
- [ ] Conferir contra `docs/DATABASE.md` seção 4 (constraints) — falta `unique_together` em `Price` (hardware + store)
- [ ] Registrar os models em `admin.py`
- [ ] Gerar migration (`makemigrations`) e validar em Docker local
- [ ] Decidir: o model `Coupon` (pertence ao app `scraping` segundo `DATABASE.md` seção 8) entra nesta branch ou vira uma sessão própria?
- [ ] Commit + PR para `develop`

### Sessão 2: `feat/builds-models`
- `Build`, `BuildComponent`, `BuildVote` (constraints: `quantity > 0`, unique por `build_id + user_id` em votes)

### Sessão 3: `feat/community-models`
- `Comment`

### Sessão 4: `feat/alerts-models`
- `PriceAlert` (unique por `user_id + hardware_id`)

### Sessão 5: `feat/coupons-model`
- `Coupon` no app `scraping` (se não entrou na Sessão 1)

> Essas quatro sessões são pequenas — bom momento para discutir se compensa agrupar 2-3 numa PR só ou manter granular por app.

---

## Fase 2 — Segurança (bloqueador)

### Sessão 6: `fix/security`

Referência completa: `docs/SECURITY_AUDIT_2026-06-03.md`. Fazer **antes** de conectar o frontend ou subir qualquer ambiente além do dev local.

- [ ] 🔴 SEC-001: nova `SECRET_KEY` sem prefixo `django-insecure-`
- [ ] 🟠 SEC-002: `DB_PASSWORD` forte (sair de `postgres/postgres`)
- [ ] 🟠 SEC-004: `ALLOWED_HOSTS` via env var
- [ ] 🟠 SEC-005: security headers no `settings.py`
- [ ] 🟠 SEC-010: `LOGGING` mínimo de segurança
- [ ] 🟡 SEC-003: credencial do CI para GitHub Secret
- [ ] 🟡 SEC-006: `django-cors-headers` configurado (nunca `CORS_ALLOW_ALL_ORIGINS`)
- [ ] 🟡 SEC-007: `sslmode=require` no banco (prod)
- [ ] 🟡 SEC-008: `pip-audit` no CI
- [ ] 🟡 SEC-009: lock file de dependências (`pip-compile` ou Poetry)
- [ ] Considerar a recomendação do audit: separar `settings/base.py` + `dev.py` + `prod.py`

---

## Fase 3 — API REST

**Depende de:** Fases 1 e 2.

### Sessão 7: `feat/hardware-api`
- Serializers + ViewSets (list/retrieve) para hardware, categories, stores, prices
- Rotas em `urls.py`
- Testar via curl/Postman/Insomnia

### Sessão 8: `feat/auth`
- Registro/login com JWT (`djangorestframework-simplejwt`), tokens em cookies `HttpOnly`
- Proteção de endpoints (`@login_required` / permission classes)
- Referência: `CLAUDE.md` Seção 8.4 (`jwt.verify()` vs `jwt.decode()`, autenticação ≠ autorização)

### Sessão 9: `feat/builds-api`
- CRUD de builds + componentes, cálculo de preço total, votos

### Sessão 10: `feat/community-api`
- Comentários, ranking (recentes/populares)

### Sessão 11: `feat/alerts-api`
- CRUD de alertas de preço

---

## Fase 4 — Qualidade e Infraestrutura (paralelo às fases acima)

### Sessão: CI/CD do zero (sessão dedicada, pendente)
- Conceitos de GitHub Actions (triggers, jobs, steps, services) partindo do zero
- Explicação do `.github/workflows/ci.yml` atual do projeto
- Construção incremental até chegar no arquivo existente

### Sessão: `chore/testing-setup`
- `pytest` + `pytest-django` + `factory-boy`, fixtures conforme `docs/TESTING.md`
- Cobertura mínima 80%, integrar checagem no CI

---

## Fase 5 — Scraping

**Depende de:** models de `hardware`, `prices`, `price_history` (Fase 1).

### Sessão: `feat/scraping-mvp`
- Scraper MVP: Terabyte + KaBuM! (BeautifulSoup/Selenium)
- Celery + Celery Beat: job diário às 03:00 BRT
- Persistir em `prices`, `price_history` e `coupons`
- Segurança: allowlist de URLs de scraping (nunca vindas de input do usuário — SSRF, ver SECURITY_AUDIT domínio 9)

---

## Fase 6 — Frontend

**Depende de:** API REST funcional (Fase 3).

### Sessão: `chore/frontend-setup`
- React + Vite + Tailwind + React Router

### Sessão: `feat/frontend-catalog`
- Home page, catálogo de hardware, filtros avançados

### Sessão: `feat/frontend-auth`
- Telas de login/registro, integração com JWT

### Sessão: `feat/frontend-builder`
- PC Builder (seleção de peças) + verificador de compatibilidade em tempo real

### Sessão: `feat/frontend-community`
- Ranking de builds, comentários, dashboard do usuário

---

## Fase 7 — Post-MVP

### Sessão: `feat/ai-recommendations`
- RAG sobre conhecimento do Reddit + Groq/Claude/Gemini para sugestões de peças
- Segurança: rate limit por usuário, `max_tokens` sempre definido, sem input direto do usuário no system prompt (CLAUDE.md Seção 8.7 e 8.6)

### Futuro (sem sessão definida ainda)
- Bot Telegram (alertas de oferta)
- Extensão de navegador (estilo Bilômetro)
- Internacionalização (i18n)

---

## Fora deste roadmap

- **Projeto de microsserviços:** decisão já tomada de manter o Hardware Tracker como monolito desacoplado. Microsserviços ficam para um **projeto futuro** dedicado, após este projeto.

---

## Notas de Processo

- **Notion:** este roadmap replica/complementa o que deveria estar sincronizado com a página "HARDWARE TRACKER" e o backlog no Notion. Na sessão em que este arquivo foi atualizado (2026-07-07), o MCP do Notion não estava autenticado — revisar manualmente se este roadmap diverge do backlog lá.
- **Arquivo `2026-06-30-proximos-passos.md`** (raiz do repo, não commitado): cobre em mais detalhe as Sessões 1, 7 e 8 deste roadmap. Considerar consolidar num só lugar para não manter duas fontes de verdade.

---

## Referências

- [DATABASE.md](DATABASE.md) — Modelagem do banco de dados
- [ARCHITECTURE.md](ARCHITECTURE.md) — Decisões arquiteturais
- [REQUIREMENTS.md](REQUIREMENTS.md) — Levantamento de requisitos
- [TESTING.md](TESTING.md) — Estratégia de testes
- [SECURITY_AUDIT_2026-06-03.md](SECURITY_AUDIT_2026-06-03.md) — Auditoria de segurança
