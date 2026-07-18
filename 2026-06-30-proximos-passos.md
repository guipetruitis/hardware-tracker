# Próximos Passos — Hardware Tracker

> **Para execução:** Cada tarefa representa uma branch separada. Abrir PR para `develop` ao concluir cada uma.

**Goal:** Evoluir o projeto do scaffold inicial para um backend funcional com Docker, modelos de banco e API REST.

**Architecture:** Django REST Framework como API, PostgreSQL via Docker Compose, CI com GitHub Actions validando cada PR.

**Tech Stack:** Python 3.12, Django 6, DRF, PostgreSQL 16, Docker, GitHub Actions

---

## Fase 1 — Infraestrutura (Imediato)

### Tarefa 1: `chore/docker-setup`

**Arquivos:**

- Commit: `backend/Dockerfile`
- Commit: `docker-compose.yml`

**O que fazer:**

- [X] Revisar o `Dockerfile` — entender cada linha (FROM, WORKDIR, COPY, RUN)
- [X] Revisar o `docker-compose.yml` — entender os serviços `db` e `web`
- [X] Criar branch: `git checkout -b chore/docker-setup`
- [X] Adicionar e commitar os dois arquivos:
  ```
  git add backend/Dockerfile docker-compose.yml
  git commit -m "chore: adiciona Dockerfile e docker-compose"
  ```
- [X] Push e abrir PR para `develop`

**Como testar:**

```bash
docker compose up --build
# Acesse http://localhost:8000 — deve retornar resposta do Django
```

---

### Tarefa 2: `chore/update-ci`

**Arquivos:**

- Modificar: `.github/workflows/ci.yml`

**O que fazer:**

- [X] Criar branch: `git checkout -b chore/update-ci`
- [X] Atualizar as actions para versões mais recentes:
  - `actions/checkout@v4` → `actions/checkout@v5`
  - `actions/setup-python@v5` → `actions/setup-python@v6`
- [X] Commitar: `chore: atualiza actions do CI para remover warning Node.js 20`
- [X] Push, abrir PR e verificar se o warning sumiu

---

## Fase 2 — Modelagem do Banco (SDLC: Modelagem)

### Tarefa 3: `feat/hardware-models`

**Arquivos:**

- Modificar: `backend/apps/hardware/models.py`
- Criar: `backend/apps/hardware/migrations/0001_initial.py` (via makemigrations)
- Modificar: `backend/apps/hardware/admin.py`

**Contexto:**
O app `hardware` é o coração do sistema — armazena os componentes de PC (processadores, GPUs, RAM, etc.) e seus preços.

**O que fazer:**

Criar branch: `git checkout -b feat/hardware-models`

Pensar e definir quais campos cada peça de hardware precisa ter (nome, marca, categoria, preço, URL, loja, etc.)

Implementar os models no `models.py`

Registrar no `admin.py` para visualizar no Django Admin

Gerar a migration: `python manage.py makemigrations`

Verificar: `python manage.py check`

Commitar e abrir PR

**Perguntas para pensar antes de modelar:**

1. Um produto pode ter múltiplos preços (uma por loja)? Como modelar isso?
2. Como representar a categoria da peça (CPU, GPU, RAM...)?
3. Quais campos são obrigatórios vs opcionais?

---

## Fase 3 — API REST (SDLC: Implementação)

### Tarefa 4: `feat/hardware-api`

**Arquivos:**

- Criar: `backend/apps/hardware/serializers.py`
- Modificar: `backend/apps/hardware/views.py`
- Modificar: `backend/config/urls.py`

**Depende de:** Tarefa 3 (models criados)

**O que fazer:**

- [ ] Criar branch: `git checkout -b feat/hardware-api`
- [ ] Criar serializers para os models de hardware
- [ ] Criar ViewSets no DRF (list, retrieve)
- [ ] Registrar as rotas no `urls.py`
- [ ] Testar os endpoints via `curl` ou Postman/Insomnia
- [ ] Commitar e abrir PR

---

## Fase 4 — Autenticação (SDLC: Implementação)

### Tarefa 5: `feat/auth`

**Arquivos:**

- Modificar: `backend/apps/users/views.py`
- Modificar: `backend/apps/users/serializers.py` (criar)
- Modificar: `backend/config/urls.py`
- Adicionar: `djangorestframework-simplejwt` no `requirements.txt`

**O que fazer:**

- [ ] Criar branch: `git checkout -b feat/auth`
- [ ] Implementar endpoints de registro e login com JWT
- [ ] Configurar `simplejwt` no `settings.py`
- [ ] Proteger endpoints que precisam de autenticação
- [ ] Testar fluxo completo: registro → login → token → requisição autenticada

**Referência de segurança (CLAUDE.md Seção 8.4):**

- JWT: sempre `jwt.verify()`, nunca `jwt.decode()` sem verificar assinatura
- Autenticação ≠ Autorização (verificar permissão em cada endpoint)

---

## Ordem sugerida

```
chore/docker-setup  →  chore/update-ci  →  feat/hardware-models  →  feat/hardware-api  →  feat/auth
```

Cada tarefa gera um PR para `develop`. A `main` só recebe merge em momento de release.