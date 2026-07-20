# Security Audit Report — Hardware Tracker

**Nível:** L2 (projeto com auth planejado, dados de usuários, integração LLM futura)  
**Projeto:** Hardware Tracker  
**Data:** 2026-06-03  
**Auditado por:** hm-security v2.3  

---

## Resumo Executivo

| Severidade | Quantidade |
|---|---|
| 🔴 CRÍTICO | 1 |
| 🟠 ALTO | 4 |
| 🟡 MÉDIO | 5 |

**Veredicto: BLOQUEADO para deploy**

> O projeto está em scaffold early-stage. Não há views, endpoints ou lógica de negócio implementados. A auditoria cobre o que existe (infra, settings, CI, secrets, planejamento) e levanta os gaps que devem ser endereçados antes de implementar cada feature.

---

## Domínios Auditados

1. Container & Infraestrutura
2. Aplicação — OWASP Top 10
5. Dados & Compliance
6. Dependências & Supply Chain
7. Secrets Management
8. Logging & Monitoramento
9. Business Logic (planejamento futuro)

---

## Domínio 7: Secrets Management

### SEC-001 — SECRET_KEY com prefixo "django-insecure" 🔴 CRÍTICO

**Onde:** `backend/.env` linha 1

```
SECRET_KEY=django-insecure-b38pb04+%@px(!2wsbnlie=aeg$u@z0qu2=k81+i2p0ub9_7u3
```

**Vulnerabilidade:** A chave gerada pelo `django-admin startproject` tem o prefixo `django-insecure-` — o próprio Django sinaliza que não é segura para produção. Se usada em produção, qualquer pessoa com acesso à chave pode forjar cookies de sessão e tokens CSRF.

**Impacto:** Comprometimento total das sessões de usuário em produção.

**Fix:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
# Resultado: nova chave sem o prefixo "django-insecure-"
# Armazenar em secrets manager (AWS SSM, Doppler) — nunca no .env commitado
```

**Referência:** Django Deployment Checklist — SECRET_KEY

---

### SEC-002 — DB_PASSWORD padrão (postgres/postgres) 🟠 ALTO

**Onde:** `backend/.env` linhas 4-5

```
DB_USER=postgres
DB_PASSWORD=postgres
```

**Vulnerabilidade:** Credenciais default do PostgreSQL. Qualquer script de ataque automatizado tenta essas credenciais primeiro.

**Impacto:** Comprometimento do banco de dados em staging/produção se não trocado.

**Fix:** Gerar senha forte antes de subir qualquer ambiente além do dev local:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## Domínio 1: Container & Infraestrutura

### SEC-003 — Credencial de banco em plaintext no CI 🟡 MÉDIO

**Onde:** `.github/workflows/ci.yml` linha 42

```yaml
POSTGRES_PASSWORD: hardware123
```

**Vulnerabilidade:** Senha de banco de dados de teste hardcoded no YAML do CI, visível no repositório.

**Impacto:** Normaliza o padrão de colocar credenciais em YAML. Em projetos que crescem, isso frequentemente evolui para credenciais reais no mesmo lugar.

**Fix:**
```yaml
POSTGRES_PASSWORD: ${{ secrets.CI_DB_PASSWORD }}
```
Configurar `CI_DB_PASSWORD` como GitHub Secret nas settings do repositório.

---

## Domínio 2: Aplicação — OWASP Top 10

### SEC-004 — ALLOWED_HOSTS vazio 🟠 ALTO

**Onde:** `backend/config/settings.py` linha 29

```python
ALLOWED_HOSTS = []
```

**Vulnerabilidade:** Com `DEBUG=False` em produção, `ALLOWED_HOSTS = []` rejeita todas as requisições. Com `DEBUG=True` (dev), aceita qualquer host — suscetível a HTTP Host Header Injection.

**Impacto:** DoS acidental em produção, ou Host Header Poisoning em dev exposto.

**Fix:**
```python
ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='localhost,127.0.0.1',
    cast=lambda v: [h.strip() for h in v.split(',')]
)
```

---

### SEC-005 — Security headers ausentes 🟠 ALTO

**Onde:** `backend/config/settings.py` (ausência)

**Vulnerabilidade:** Nenhum dos security headers do Django está configurado. O middleware `SecurityMiddleware` está presente mas sem as configurações que o ativam.

**Impacto:** Exposição a clickjacking, MIME sniffing, ausência de HSTS, cookies sem flags de segurança.

**Fix — adicionar ao settings.py:**
```python
# Headers de segurança (sempre)
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SESSION_COOKIE_HTTPONLY = True

# Apenas em produção (settings_prod.py):
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

**Referência:** OWASP A05:2021 — Security Misconfiguration

---

### SEC-006 — CORS não planejado 🟡 MÉDIO

**Onde:** `backend/requirements.txt` (ausência de `django-cors-headers`)

**Vulnerabilidade:** O projeto usa DRF mas não tem CORS configurado. Quando o frontend React for conectado, há risco de adicionar `CORS_ALLOW_ALL_ORIGINS = True` às pressas.

**Impacto:** API aberta para qualquer origem — qualquer site pode fazer requests autenticadas em nome do usuário.

**Fix — instalar agora e configurar corretamente:**
```bash
pip install django-cors-headers
```
```python
# settings.py
INSTALLED_APPS = [..., 'corsheaders']
MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware', ...]  # deve ser o PRIMEIRO

# Nunca usar CORS_ALLOW_ALL_ORIGINS = True em produção
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    cast=lambda v: [h.strip() for h in v.split(',')]
)
```

---

## Domínio 5: Dados & Compliance

### SEC-007 — Sem SSL no banco de dados 🟡 MÉDIO

**Onde:** `backend/config/settings.py` linhas 83-92

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        # ← sem 'OPTIONS': {'sslmode': 'require'}
    }
}
```

**Vulnerabilidade:** Conexão com o banco sem SSL expõe dados em trânsito a ataques man-in-the-middle na rede.

**Impacto:** Queries, resultados e credenciais trafegam em plaintext entre app e banco.

**Fix:**
```python
'OPTIONS': {
    'sslmode': config('DB_SSL_MODE', default='require'),
}
```

---

## Domínio 6: Dependências & Supply Chain

### SEC-008 — Sem pip-audit no CI 🟡 MÉDIO

**Onde:** `.github/workflows/ci.yml`

**Vulnerabilidade:** O CI roda apenas `flake8` e testes. Nenhum scan de vulnerabilidades em dependências.

**Impacto:** CVEs em `Django`, `djangorestframework` ou `psycopg2` passam despercebidos.

**Fix — adicionar step ao ci.yml:**
```yaml
- name: Security audit (dependências)
  run: |
    pip install pip-audit
    pip-audit -r backend/requirements.txt
```

---

### SEC-009 — Sem lock file de produção 🟡 MÉDIO

**Onde:** `backend/requirements.txt`

**Vulnerabilidade:** O `requirements.txt` fixa versões diretas (`Django==6.0.5`), mas sub-dependências podem resolver versões diferentes em builds futuros.

**Impacto:** Reprodutibilidade de build comprometida; uma sub-dependência pode introduzir CVE entre deploys.

**Fix:** Migrar para `poetry` ou usar `pip-compile` para gerar `requirements.lock`:
```bash
pip install pip-tools
pip-compile backend/requirements.txt -o backend/requirements.lock
```

---

## Domínio 8: Logging & Monitoramento

### SEC-010 — Sem logging de segurança configurado 🟠 ALTO

**Onde:** `backend/config/settings.py` (ausência de `LOGGING`)

**Vulnerabilidade:** Sem configuração de `LOGGING`, eventos de segurança (falhas de autenticação, erros 5xx, violations de CSRF) vão silenciosamente para stderr sem estrutura ou retenção.

**Impacto:** Impossível detectar ataques de força bruta, probing de endpoints, ou incidents em produção.

**Fix mínimo:**
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.security': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}
```

---

## Domínio 9: Planejamento — Flags para Features Futuras

> Esses não são findings do código atual — são alertas para acionar o checklist de segurança **antes de implementar** cada feature.

| Feature Planejada | Risco Principal | Ação Antes de Codar |
|---|---|---|
| Autenticação de usuários | A07 — Auth Failures | Usar `django-allauth` ou `dj-rest-auth`; tokens em cookies `HttpOnly`, nunca `localStorage` |
| Web Scraping | SSRF | URLs de scraping devem vir de allowlist configurada, nunca de input do usuário |
| IA/LLM (Groq, Claude, Gemini) | Domínio 12 completo | Rate limit por usuário, `max_tokens` sempre definido, sem user input direto no system prompt |
| Upload de imagens de builds | Domínio 11 completo | UUID no filename, validação por magic bytes, reprocessar com Pillow, strip EXIF |
| Sistema de cupons / preços | Business Logic | Preços **sempre** no servidor; cupons com expiração e single-use enforced no banco |
| Admin panel Django | A01 — Broken Access Control | Trocar URL padrão `/admin/`, restringir por IP em produção, habilitar 2FA para superusers |

---

## Avaliação do Planejamento de Segurança (CLAUDE.md Seção 8)

O planejamento documentado na Seção 8 do `CLAUDE.md` é **sólido e completo**. Cobre os 11 domínios relevantes, tem checklist pré-deploy bem estruturado, e referencia fontes corretas (Mayk Brito, OWASP Top 10, OWASP LLM Top 10).

**O gap não está no planejamento — está na execução do scaffold.**

O `settings.py` gerado pelo `django-admin` é um ponto de partida razoável (usa `python-decouple`, `DEBUG=False` como default, validators de password), mas faltam os security headers e o `LOGGING` que o próprio `CLAUDE.md` já prevê.

### Próximo Passo Recomendado

Antes de implementar qualquer feature, criar a estrutura de settings separada:

```
backend/config/
├── settings/
│   ├── __init__.py
│   ├── base.py       ← o que existe hoje + security headers
│   ├── dev.py        ← DEBUG=True, sem SSL redirect
│   └── prod.py       ← DEBUG=False, HTTPS obrigatório, logging completo
```

Assim cada feature nasce dentro de um contexto seguro, não fora dele.

---

## Checklist de Resolução

```
CRÍTICO (antes de qualquer deploy):
☐ SEC-001: Gerar SECRET_KEY nova sem prefixo "django-insecure-"

ALTO (antes de conectar o frontend):
☐ SEC-002: Trocar DB_PASSWORD=postgres por senha forte
☐ SEC-004: Configurar ALLOWED_HOSTS via env var
☐ SEC-005: Adicionar security headers ao settings.py
☐ SEC-010: Configurar LOGGING mínimo de segurança

MÉDIO (próximo sprint):
☐ SEC-003: Mover CI_DB_PASSWORD para GitHub Secret
☐ SEC-006: Instalar e configurar django-cors-headers
☐ SEC-007: Migrar para poetry ou pip-compile
☐ SEC-008: Adicionar pip-audit ao CI
☐ SEC-009: Configurar sslmode=require para produção
```
