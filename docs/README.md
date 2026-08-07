# Documentação - Hardware Tracker

Bem-vindo à documentação centralizada do projeto Hardware Tracker! Este diretório contém toda a documentação estruturada para orientar o desenvolvimento.

---

## 📚 Índice de Documentos

### 1. **REQUIREMENTS.md** — Levantamento de Requisitos
   - **Status:** ✅ Completo
   - **Fase SDLC:** Levantamento de Requisitos
   - **Conteúdo:**
     - Visão geral do projeto
     - Funcionalidades principais (core, PC Builder, distribuição)
     - Componentes suportados
     - Estrutura de telas (Home, Login, etc.)
     - Requisitos de UI/UX
     - Lojas e integrações
     - Critérios de aceitação (MVP vs Post-MVP)
     - Priorização de features

   **Quando consultar:**
   - Início de nova feature/tarefa
   - Dúvidas sobre escopo
   - Validação de requisitos

   **Relacionados:** CLAUDE.md (contexto)

---

### 2. **ARCHITECTURE.md** — Arquitetura do Sistema
   - **Status:** 🔄 Em Planejamento
   - **Fase SDLC:** Modelagem & Design
   - **Conteúdo:**
     - Diagrama de arquitetura (Frontend, Backend, Database, Services)
     - Componentes principais (Frontend, Backend, DB)
     - Padrões de design (MVC, Service Layer, Repository Pattern)
     - Fluxos de dados (Build creation, Scraping, IA suggestions)
     - Decisões técnicas com tradeoffs
       - Frontend Framework (React vs Vue vs Svelte)
       - State Management (Redux vs Context vs Zustand)
       - Autenticação (Session vs JWT)
       - Caching (Redis vs Django ORM)
       - Task Queue (Celery vs Django-RQ)
     - Infraestrutura (Local com Docker, Produção com AWS)
     - Segurança (HTTPS, CSRF, XSS, Rate Limiting)
     - Performance (Caching, Indexing, Lazy Loading)

   **Quando consultar:**
   - Antes de começar implementação
   - Quando precisar entender fluxo de dados
   - Para revisar decisões arquiteturais

   **Relacionados:** DATABASE.md, TESTING.md

---

### 3. **DATABASE.md** — Modelagem de Banco de Dados
   - **Status:** 🔄 Em Planejamento
   - **Fase SDLC:** Modelagem & Design
   - **Conteúdo:**
     - Diagrama ER (Entidade-Relacionamento)
     - Definição de 10+ tabelas principais:
       - users, categories, hardware, stores
       - prices, price_history, builds, build_components
       - comments, compatibility_rules
     - SQL DDL completo para cada tabela
     - Constraints e validações
     - Índices criados e razão
     - Operações comuns (queries úteis)
     - Decisões de design (JSONB, soft_delete, denormalização)
     - Migrations com Django

   **Quando consultar:**
   - Durante modelagem de dados
   - Antes de criar models Django
   - Para entender relacionamentos

   **Relacionados:** ARCHITECTURE.md, REQUIREMENTS.md

---

### 4. **ROADMAP.md** — Próximos Passos
   - **📍 Onde está:** `.brain-hardwaretracker/ROADMAP.md` — **não está em `docs/`**. Mora no vault Obsidian local, que é ignorado pelo git (ver `.gitignore`)
   - **Status:** ✅ Atualizado (2026-08-05 — cronograma até o lançamento de 15/09)
   - **Fase SDLC:** Planejamento Contínuo
   - **Conteúdo:**
     - Estado atual do projeto
     - Blocos de trabalho priorizados (Backend, API, Infra, Frontend, Scraping)
     - Checklist de tarefas pendentes por bloco

   **Quando consultar:**
   - Início de sessão (o que fazer a seguir?)
   - Após concluir uma tarefa (o que vem depois?)

   **Relacionados:** DATABASE.md, ARCHITECTURE.md, REQUIREMENTS.md

---

### 5. **TESTING.md** — Estratégia de Testes
   - **Status:** 🔄 Em Planejamento
   - **Fase SDLC:** Testes & Review
   - **Conteúdo:**
     - Pirâmide de testes (70% Unit, 25% Integration, 5% E2E)
     - Testes Unitários (pytest, pytest-django, factory-boy)
     - Testes de Integração (API tests, DB tests)
     - Testes E2E (Selenium, fluxos críticos)
     - Testes de Segurança (OWASP Top 10)
     - Testes de Performance (Locust, métricas alvo)
     - Testes Manuais (QA checklist)
     - CI/CD com GitHub Actions
     - Cobertura de testes (meta: 80%)

   **Quando consultar:**
   - Antes de codificar uma feature
   - Para planejar testes
   - Durante code review

   **Relacionados:** REQUIREMENTS.md, ARCHITECTURE.md

---

### 6. **BACKEND_PRINCIPLES.md** — Princípios de Backend
   - **📍 Onde está:** `.brain-hardwaretracker/Wiki/BACKEND_PRINCIPLES.md` — **não está em `docs/`**. Mora no vault Obsidian local, que é ignorado pelo git (ver `.gitignore`)
   - **Status:** ✅ Vivo (revisar a cada bloco do ROADMAP)
   - **Fase SDLC:** Transversal (Design → Implementação → Deploy → Operação)
   - **Conteúdo:**
     - Os 10 pilares de um backend profissional, cruzados com o estado real do código
     - Por pilar: o conceito, como quebra na prática, o que existe hoje, o que falta
     - Lacunas descobertas (L-01 a L-06) com prioridade e momento de decidir
     - Checklist de maturidade de backend (irmão do checklist de segurança do CLAUDE.md §8.10)
     - Perguntas em aberto que viram decisão/ADR

   **Quando consultar:**
   - Antes de implementar escrita no banco, job assíncrono ou endpoint novo
   - Antes do deploy (rodar o checklist de maturidade)
   - Depois do deploy, para diagnosticar o que o sistema não conta sobre si mesmo
   - Ao revisar se uma entrega está de fato de pé, e não só "funcionando no localhost"

   **Relacionados:** ARCHITECTURE.md, DATABASE.md, TESTING.md, ROADMAP.md, CLAUDE.md §8

---

## 🔄 Fluxo de Trabalho Recomendado

### Para Uma Nova Feature:

1. **Levantamento** → Ler `REQUIREMENTS.md`
   - Confirmar escopo
   - Validar prioridade
   - Entender critérios de aceitação

2. **Modelagem** → Consultar `ARCHITECTURE.md` + `DATABASE.md`
   - Entender onde encaixa na arquitetura
   - Identificar novas tabelas/relacionamentos
   - Revisar padrões de design

3. **Planejamento de Testes** → Ler `TESTING.md`
   - Definir testes unitários necessários
   - Planejar testes de integração
   - Considerar testes E2E críticos

4. **Implementação** → Desenvolver código
   - Seguir padrões de ARCHITECTURE.md
   - Implementar testes primeiro (TDD)
   - Fazer commits com mensagens claras

5. **Review** → Code Review
   - Verificar cobertura de testes
   - Validar contra requisitos
   - Revisar segurança

---

## 📋 Status da Documentação

| Documento | Status | Versão | Última Atualização |
|-----------|--------|--------|-------------------|
| REQUIREMENTS.md | ✅ Completo | 1.0 | 2026-05-15 |
| ARCHITECTURE.md | 🔄 Em Planejamento | 0.1 | 2026-05-15 |
| DATABASE.md | 🔄 Em Planejamento | 0.1 | 2026-05-15 |
| TESTING.md | 🔄 Em Planejamento | 0.1 | 2026-05-15 |
| ROADMAP.md | ✅ Atualizado | — | 2026-08-05 |
| BACKEND_PRINCIPLES.md | ✅ Vivo | 1.0 | 2026-08-06 |

> **📍 Dois destes documentos não vivem em `docs/`:** o `ROADMAP.md` está em `.brain-hardwaretracker/ROADMAP.md` e o `BACKEND_PRINCIPLES.md` em `.brain-hardwaretracker/Wiki/BACKEND_PRINCIPLES.md`. O vault Obsidian é local e ignorado pelo git, então quem clonar este repositório **não** vai encontrá-los — não é arquivo faltando, é escolha de onde eles moram.

---

## 🛠 Ferramentas de Geração/Consulta

Ao trabalhar com estes documentos, você pode usar:

| Ferramenta | Para | Comando |
|-----------|------|---------|
| `/figma-*` | Criar diagramas de arquitetura | Consultar CLAUDE.md seção 6 |
| `Context7` | Documentação de Django, PostgreSQL, React | Integrado no ambiente |
| `obsidian-cli` | Sincronizar com notas pessoais | Skill disponível |
| `json-canvas` | Diagramas visuais (fluxos, etc.) | Skill disponível |
| GitHub | Versionamento de documentação | commit messages claros |

---

## 🔗 Links Relacionados

- **[CLAUDE.md](../CLAUDE.md)** — Guia de atuação da IA (orquestrador geral)
- **[Memory System](C:\Users\Guilherme\.claude\projects\c--Users-Guilherme-Documents-Dev-2026-project001-hardware-tracker\memory\MEMORY.md)** — Contexto persistente do projeto
- **[GitHub Repository](https://github.com/)** — Versionamento do código (a definir)
- **[Figma Design](https://figma.com/)** — Protótipos UI/UX (a definir)
- **[n8n Workflows](https://n8n.io/)** — Automações (a definir)

---

## ❓ Perguntas Frequentes

**P: Qual documento devo ler primeiro?**  
R: REQUIREMENTS.md. Ele dá contexto do projeto inteiro.

**P: Como estes documentos se relacionam?**  
R: REQUIREMENTS defini WHAT (o quê fazer). ARCHITECTURE defini HOW (como fazer). DATABASE defini WHERE (onde armazenar). TESTING defini VERIFY (como validar).

**P: Com que frequência atualizar?**  
R: Após cada decisão importante ou mudança de escopo. Usar git history para rastrear mudanças.

**P: Posso usar outros formatos (Markdown, Diagrams, etc.)?**  
R: Sim! Recomenda-se manter aqui versão "master" mas usar Figma, draw.io, etc. para diagramas detalhados.

---

## 📝 Como Contribuir

Ao atualizar documentação:

1. Editar o arquivo relevante
2. Atualizar "Última Atualização" e versão
3. Commit com mensagem clara: `docs: update ARCHITECTURE.md with API design`
4. Link em MEMORY.md se for decisão importante

---

## 🎯 Próximos Passos (Roadmap)

- [ ] Validar ARCHITECTURE.md com decisões finais
- [ ] Implementar migrations Django baseadas em DATABASE.md
- [ ] Configurar pytest conforme TESTING.md
- [ ] Criar Figma designs baseados em REQUIREMENTS.md
- [ ] Expandir TESTING.md com exemplos reais
- [ ] Documentar CI/CD em ARCHITECTURE.md

---

**Última revisão:** 2026-05-15  
**Responsável:** Guilherme (via IA Mentor)  
**Versão da Documentação:** 0.2
