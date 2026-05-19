# Modelagem de Banco de Dados - Hardware Tracker

**Status:** Em Planejamento  
**Última Atualização:** 2026-05-15  
**Versão:** 0.1 (Draft)  
**SGBD:** PostgreSQL 13+

---

## 1. Diagrama ER (Entidade-Relacionamento)

```
┌────────────────┐         ┌──────────────┐
│     User       │◄────────┤   Build      │
├────────────────┤         ├──────────────┤
│ id (PK)        │         │ id (PK)      │
│ email (UNIQUE) │         │ user_id (FK) │
│ username       │         │ name         │
│ password_hash  │         │ description  │
│ created_at     │         │ created_at   │
│ updated_at     │         │ updated_at   │
└────────────────┘         └──────────────┘
                                   │
                                   │1:N
                                   ▼
                            ┌──────────────┐
                            │ BuildComponent
                            ├──────────────┤
                            │ id (PK)      │
                            │ build_id (FK)│
                            │ hardware_id(FK)
                            │ quantity     │
                            └──────────────┘
                                   │
                                   │ M:1
                                   ▼
        ┌──────────────────────────────────────┐
        │          Hardware                    │
        ├──────────────────────────────────────┤
        │ id (PK)                              │
        │ name                                 │
        │ category_id (FK)                     │
        │ manufacturer                         │
        │ specifications (JSONB)               │
        │ compatibility_group (FK, optional)   │
        │ created_at                           │
        │ updated_at                           │
        └──────────────────────────────────────┘
                 │                       │
                 │ 1:N                   │ 1:N
                 ▼                       ▼
        ┌────────────────┐    ┌──────────────────┐
        │  PriceHistory  │    │ Price (atual)    │
        ├────────────────┤    ├──────────────────┤
        │ id (PK)        │    │ id (PK)          │
        │ hardware_id(FK)│    │ hardware_id (FK) │
        │ store_id (FK)  │    │ store_id (FK)    │
        │ price          │    │ price            │
        │ date           │    │ url              │
        │ currency       │    │ last_updated     │
        └────────────────┘    └──────────────────┘
                 │                       │
                 └───────────┬───────────┘
                             │
                             │ M:1
                             ▼
                      ┌────────────────┐
                      │    Store       │
                      ├────────────────┤
                      │ id (PK)        │
                      │ name           │
                      │ url            │
                      │ logo_url       │
                      └────────────────┘

┌──────────────────────────────────────┐
│        Comment                       │
├──────────────────────────────────────┤
│ id (PK)                              │
│ build_id (FK)                        │
│ user_id (FK)                         │
│ content                              │
│ created_at                           │
│ updated_at                           │
└──────────────────────────────────────┘

┌────────────────────────────────────────┐
│          Category                      │
├────────────────────────────────────────┤
│ id (PK)                                │
│ name (Processador, GPU, RAM, etc.)     │
│ slug                                   │
│ icon_url                               │
└────────────────────────────────────────┘

┌────────────────────────────────────────┐
│      CompatibilityRule                 │
├────────────────────────────────────────┤
│ id (PK)                                │
│ from_hardware_id (FK)                  │
│ to_hardware_id (FK)                    │
│ is_compatible (bool)                   │
│ reason (texto de explicação)           │
└────────────────────────────────────────┘
```

---

## 2. Tabelas Principais

### 2.1 Users

```sql
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    avatar_url VARCHAR(500),
    bio TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    is_staff BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
```

### 2.2 Categories

```sql
CREATE TABLE categories (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    slug VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    icon_url VARCHAR(500),
    order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_categories_slug ON categories(slug);
```

### 2.3 Hardware

```sql
CREATE TABLE hardware (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category_id BIGINT NOT NULL REFERENCES categories(id),
    manufacturer VARCHAR(100),
    model VARCHAR(100),
    sku VARCHAR(100),
    specifications JSONB, -- {"ram": "16GB", "freq": "3600MHz", etc}
    image_url VARCHAR(500),
    description TEXT,
    compatibility_group VARCHAR(50), -- "SOCKET_AM4", "DDR4", etc
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

CREATE INDEX idx_hardware_category ON hardware(category_id);
CREATE INDEX idx_hardware_manufacturer ON hardware(manufacturer);
CREATE INDEX idx_hardware_compat_group ON hardware(compatibility_group);
```

### 2.4 Stores

```sql
CREATE TABLE stores (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    slug VARCHAR(100) NOT NULL UNIQUE,
    url VARCHAR(500),
    logo_url VARCHAR(500),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Lojas iniciais: Terabyte, Kabum, Amazon, Pichau
```

### 2.5 Prices

```sql
CREATE TABLE prices (
    id BIGSERIAL PRIMARY KEY,
    hardware_id BIGINT NOT NULL REFERENCES hardware(id),
    store_id BIGINT NOT NULL REFERENCES stores(id),
    price DECIMAL(10, 2) NOT NULL,
    original_price DECIMAL(10, 2),
    in_stock BOOLEAN DEFAULT TRUE,
    product_url VARCHAR(500),
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(hardware_id, store_id)
);

CREATE INDEX idx_prices_hardware ON prices(hardware_id);
CREATE INDEX idx_prices_store ON prices(store_id);
CREATE INDEX idx_prices_updated ON prices(updated_at DESC);
```

### 2.6 PriceHistory

```sql
CREATE TABLE price_history (
    id BIGSERIAL PRIMARY KEY,
    hardware_id BIGINT NOT NULL REFERENCES hardware(id),
    store_id BIGINT NOT NULL REFERENCES stores(id),
    price DECIMAL(10, 2) NOT NULL,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (hardware_id, store_id) REFERENCES prices(hardware_id, store_id)
);

CREATE INDEX idx_price_history_hardware_date ON price_history(hardware_id, recorded_at DESC);
CREATE INDEX idx_price_history_date ON price_history(recorded_at DESC);
```

### 2.7 Builds

```sql
CREATE TABLE builds (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    total_price DECIMAL(12, 2),
    is_public BOOLEAN DEFAULT TRUE,
    views_count INT DEFAULT 0,
    likes_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

CREATE INDEX idx_builds_user ON builds(user_id);
CREATE INDEX idx_builds_public_date ON builds(is_public, created_at DESC);
```

### 2.8 BuildComponents

```sql
CREATE TABLE build_components (
    id BIGSERIAL PRIMARY KEY,
    build_id BIGINT NOT NULL REFERENCES builds(id) ON DELETE CASCADE,
    hardware_id BIGINT NOT NULL REFERENCES hardware(id),
    quantity INT DEFAULT 1,
    price_at_creation DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(build_id, hardware_id)
);

CREATE INDEX idx_build_components_build ON build_components(build_id);
```

### 2.9 Comments

```sql
CREATE TABLE comments (
    id BIGSERIAL PRIMARY KEY,
    build_id BIGINT NOT NULL REFERENCES builds(id) ON DELETE CASCADE,
    user_id BIGINT NOT NULL REFERENCES users(id),
    content TEXT NOT NULL,
    parent_id BIGINT REFERENCES comments(id) ON DELETE CASCADE, -- Para respostas
    likes_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

CREATE INDEX idx_comments_build ON comments(build_id);
CREATE INDEX idx_comments_user ON comments(user_id);
CREATE INDEX idx_comments_date ON comments(created_at DESC);
```

### 2.10 CompatibilityRules

```sql
CREATE TABLE compatibility_rules (
    id BIGSERIAL PRIMARY KEY,
    from_hardware_id BIGINT NOT NULL REFERENCES hardware(id),
    to_hardware_id BIGINT NOT NULL REFERENCES hardware(id),
    is_compatible BOOLEAN NOT NULL,
    reason VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(from_hardware_id, to_hardware_id)
);

CREATE INDEX idx_compat_from ON compatibility_rules(from_hardware_id);
CREATE INDEX idx_compat_to ON compatibility_rules(to_hardware_id);
```

---

## 3. Constraints e Validações

| Tabela | Constraint | Tipo | Descrição |
|--------|-----------|------|-----------|
| users | email | UNIQUE | Email não pode se repetir |
| users | password_hash | NOT NULL | Senha obrigatória |
| hardware | name | NOT NULL | Nome obrigatório |
| prices | price | > 0 | Preço deve ser positivo |
| builds | user_id | FK | Build deve ter dono |
| build_components | quantity | > 0 | Quantidade mínima 1 |

---

## 4. Índices Criados

| Índice | Tabela | Colunas | Razão |
|--------|--------|---------|-------|
| idx_users_email | users | email | Busca por email (login) |
| idx_hardware_category | hardware | category_id | Filtro por categoria |
| idx_prices_updated | prices | updated_at DESC | Preços recentes |
| idx_builds_public_date | builds | is_public, created_at DESC | Ranking de builds |
| idx_comments_build | comments | build_id | Comentários por build |
| idx_price_history_date | price_history | recorded_at DESC | Histórico ordenado |

---

## 5. Operações Comuns

### 5.1 Buscar Preço Mais Barato para um Hardware

```sql
SELECT h.name, s.name as store, p.price, p.product_url
FROM prices p
JOIN hardware h ON p.hardware_id = h.id
JOIN stores s ON p.store_id = s.id
WHERE h.id = $1
ORDER BY p.price ASC
LIMIT 1;
```

### 5.2 Ranking de Builds Mais Recentes

```sql
SELECT b.*, COUNT(c.id) as comment_count
FROM builds b
LEFT JOIN comments c ON b.id = c.build_id
WHERE b.is_public = TRUE
GROUP BY b.id
ORDER BY b.created_at DESC
LIMIT 10;
```

### 5.3 Verificar Compatibilidade entre Componentes

```sql
SELECT cr.is_compatible, cr.reason
FROM compatibility_rules cr
WHERE (cr.from_hardware_id = $1 AND cr.to_hardware_id = $2)
OR (cr.from_hardware_id = $2 AND cr.to_hardware_id = $1)
LIMIT 1;
```

### 5.4 Histórico de Preços (últimos 30 dias)

```sql
SELECT hardware_id, store_id, AVG(price) as avg_price, 
       MIN(price) as min_price, MAX(price) as max_price
FROM price_history
WHERE recorded_at >= NOW() - INTERVAL '30 days'
GROUP BY hardware_id, store_id
ORDER BY recorded_at DESC;
```

---

## 6. Decisões de Design

### 6.1 JSONB para Especificações

**Por quê?** Hardware tem especificações variadas (processador: GHz/cores, RAM: GB/freq, GPU: VRAM/arch, etc.)
- Flexibilidade: não precisa criar colunas para cada especificação
- Indexável: PostgreSQL permite índices em JSONB
- Alternativa: criar tabela separada (mais normalizado mas mais joins)

### 6.2 soft_delete (deleted_at)

**Por quê?** Facilita auditoria e evita cascata de deletes
- Manter histórico para relatórios
- Recuperação acidental de dados

### 6.3 Denormalização de Preços

**Por quê?** Tabelas `prices` e `price_history`
- `prices` — dado atual (único registro por hardware/store)
- `price_history` — histórico completo
- Otimiza buscas recentes vs. análise de série temporal

---

## 7. Migrations (Django)

Usar `Django Migrations` para versionamento de schema:

```bash
python manage.py makemigrations auth hardware builds community
python manage.py migrate
```

---

## 8. Próximos Passos

1. [ ] Revisar e validar esquema com stakeholders
2. [ ] Implementar migrations Django
3. [ ] Criar modelos Django (models.py)
4. [ ] Implementar validações em nível de ORM
5. [ ] Configurar fixtures para dados de teste
6. [ ] Testar queries de performance

---

## 9. Referências

- [PostgreSQL JSON Support](https://www.postgresql.org/docs/current/datatype-json.html)
- [Django Models](https://docs.djangoproject.com/en/stable/topics/db/models/)
- [Database Normalization](https://en.wikipedia.org/wiki/Database_normalization)
