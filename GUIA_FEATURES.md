# Guia de Features — Hardware Tracker

## Exemplo: Começar uma Feature

**Cenário:** Vou trabalhar na feature "Comparador de Preços"

### Passo 1: Levantamento
```
Abrir: docs/REQUIREMENTS.md
└─ Buscar: "Comparador de Preços"
   ├─ Entender requisitos
   ├─ Ver prioridade (Alta)
   ├─ Validar critérios de aceitação
   └─ Identificar sprint
```

### Passo 2: Modelagem
```
Abrir: docs/ARCHITECTURE.md
└─ Entender:
   ├─ Fluxo de dados (scraping)
   ├─ APIs necessárias
   ├─ Decisões técnicas (Redis caching, Celery tasks)
   └─ Padrões de design

Abrir: docs/DATABASE.md
└─ Entender:
   ├─ Tabelas: hardware, prices, price_history, stores
   ├─ Relacionamentos
   └─ Queries úteis (ex: buscar preço mais barato)
```

### Passo 3: Prototipação (se UI)
```
Usar: /figma-use (skill)
└─ Criar mockup do comparador de preços
   ├─ Tabela com lojas e preços
   ├─ Filtros
   └─ Validar com REQUIREMENTS.md
```

### Passo 4: Testes
```
Abrir: docs/TESTING.md
└─ Planejar testes:
   ├─ Unit test: função de cálculo de melhor preço
   ├─ Integration test: API GET /hardware/{id}/prices
   ├─ E2E test: usuário vê preços por loja
   └─ Performance test: scraping < 5min
```

### Passo 5: Implementação
```
Coding:
├─ Escrever testes primeiro (TDD)
├─ Implementar service de preços
├─ Criar API endpoints
├─ Validar contra requisitos
└─ Fazer commits com mensagens claras
```

### Passo 6: Documentação
```
Atualizar:
├─ Se novo schema: adicionar a DATABASE.md
├─ Se nova API: adicionar a ARCHITECTURE.md
├─ Se achado importante: atualizar Memory
└─ Fazer commit final
```

---

## Dicas Importantes

### 1. NUNCA pule fases do SDLC
```
Errado: Começar a codificar sem requisitos claros
Certo:  Ler REQUIREMENTS.md → ARCHITECTURE.md → depois coding
```

### 2. Sempre consultar documentação antes de decidir
```
Errado: "Vou usar Redux porque conheço"
Certo:  Ler ARCHITECTURE.md → ver tradeoffs → decidir com contexto
```

### 3. A IA guia, não implementa
```
Errado: "Me implementa essa feature"
Certo:  "Como devo arquitetar esse módulo?" → Discuss → Você codifica
```

### 4. Manter documentação atualizada
```
Errado: Deixar docs desatualizado
Certo:  Atualizar docs com decisões importantes
```

---

## Perguntas Frequentes

**P: Por onde começo?**
R: Leia `CLAUDE.md` completamente, depois consulte `docs/REQUIREMENTS.md`.

**P: Posso pular ARCHITECTURE.md?**
R: Não recomendado. Vai economizar tempo agora mas causar problemas depois.

**P: E se quiser só codificar?**
R: A IA vai guiar você através das fases. Coding vem no final!

**P: Como atualizar documentação?**
R: Editar arquivo correspondente, atualizar versão, fazer commit descritivo.

**P: Posso usar outras ferramentas (draw.io, Miro, etc.)?**
R: Sim! Manter versão "master" em markdown aqui, mas usar ferramentas avançadas para design.

---

## Aprendizado Progressivo

Este projeto foi estruturado para **você aprender** enquanto desenvolve:

```
Fase                  Aprendizado
─────────────────────────────────────────
Levantamento          Como fazer requisitos
Modelagem             Arquitetura e design patterns
Prototipação          UI/UX e feedback
Testes                TDD e quality assurance
Implementação         Boas práticas de código
Documentação          Comunicação técnica
```

A IA vai guiar cada fase, explicando tradeoffs e por que cada decisão foi tomada.
