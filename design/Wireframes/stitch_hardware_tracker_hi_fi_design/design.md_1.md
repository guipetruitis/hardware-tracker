# Design System — Hardware Tracker

**Status:** Em Progresso  
**Última Atualização:** 2026-05-18  
**Versão:** 0.1

---

## 1. Identidade Visual

### 1.1 Paleta de Cores

| Token          | Hex       | Uso                                      |
|----------------|-----------|------------------------------------------|
| `bg-base`      | `#FFFFFF` | Fundo principal da aplicação             |
| `bg-section`   | `#F5F5F7` | Fundo de seções alternadas               |
| `bg-card`      | `#FFFFFF` | Fundo de cards e painéis                 |
| `primary`      | `#FF6B00` | Ações primárias, links, destaques        |
| `secondary`    | `#E63946` | Tags, badges secundários, alertas        |
| `success`      | `#22C55E` | Badges de desconto, compatibilidade OK   |
| `danger`       | `#E63946` | Incompatibilidade, erros                 |
| `text-primary` | `#1A1A1A` | Títulos e textos principais              |
| `text-muted`   | `#6B7280` | Subtítulos, labels, metadados            |
| `border`       | `#E5E7EB` | Bordas de cards e divisórias             |
| `footer-bg`    | `#1A1A1A` | Fundo do rodapé                          |

### 1.2 Tipografia

| Elemento     | Fonte | Tamanho | Peso      |
|--------------|-------|---------|-----------|
| H1 (Hero)    | Inter | 64px    | Bold      |
| H2 (Seção)   | Inter | 32px    | Bold      |
| H3 (Card)    | Inter | 20px    | Semi Bold |
| Body         | Inter | 16px    | Regular   |
| Small / Label| Inter | 13px    | Regular   |
| Badge / Tag  | Inter | 12px    | Medium    |
| Navbar links | Inter | 14px    | Medium    |

### 1.3 Espaçamento

- **Grid:** 12 colunas, gutter 24px, margem lateral 80px (desktop 1440px)
- **Seções:** padding vertical de 80px entre seções
- **Cards:** padding interno de 20px, gap entre cards de 24px
- **Border radius:** 8px (botões/inputs), 12px (cards), 14px (badges)

### 1.4 Sombras e Efeitos

- Cards com `box-shadow: 0 2px 12px rgba(0,0,0,0.08)` e borda `1px solid #E5E7EB`
- Hover em cards: `box-shadow: 0 8px 24px rgba(255, 107, 0, 0.12)`
- Botão primário: fundo `#FF6B00`, hover `#E55F00`
- Gradiente hero: linear suave de `#FFFFFF` para `#FFF4EC`
- Faixa de estatísticas: fundo sólido `#FF6B00`, texto branco

---

## 2. Componentes

### 2.1 Botões

| Variante    | Fundo     | Texto   | Borda              |
|-------------|-----------|---------|---------------------|
| Primary     | `#4F6EF7` | Branco  | Nenhuma             |
| Secondary   | `#1A1A2E` | Muted   | `1px #2A2A3E`       |
| Ghost       | Transparente | Primary | `1px #4F6EF7`   |
| Danger      | `#F75F5F` | Branco  | Nenhuma             |

Altura padrão: 48px (large), 36px (medium), 28px (small)

### 2.2 Cards

- **Product Card:** imagem, nome, loja, preço atual, preço antigo, badge de desconto, CTA
- **Build Card:** preview, nome da build, autor, preço total, likes, tags
- **Feature Card:** ícone com fundo translúcido, título, descrição curta
- **Stats Card:** número grande, label descritivo

### 2.3 Badges / Tags

- Fundo: cor de destaque com 20% de opacidade
- Borda: cor de destaque com 40% de opacidade
- Texto: cor de destaque em 100%
- Exemplos: `Gamer`, `4K`, `Budget`, `−12%`, `#1`

### 2.4 Inputs

- Fundo: `#0D0D0F`
- Borda: `1px solid #2A2A3E`
- Focus: `1px solid #4F6EF7`
- Placeholder: `#8B8FA8`
- Altura: 48px, border radius: 8px

---

## 3. Telas Planejadas

| Tela                   | Prioridade | Status         | Arquivo                              |
|------------------------|-----------|----------------|--------------------------------------|
| Home Page              | Alta      | Wireframe OK   | `design/wireframe-home-lofi.html`    |
| Login / Cadastro       | Alta      | Pendente       | —                                    |
| PC Builder             | Alta      | Pendente       | —                                    |
| Página de Peça         | Alta      | Pendente       | —                                    |
| Comunidade / Ranking   | Média     | Pendente       | —                                    |
| Dashboard do Usuário   | Média     | Pendente       | —                                    |

---

## 4. Fluxo de Navegação (MVP)

```
Home
├── → PC Builder (CTA hero / navbar)
├── → Página de Peça (card de oferta)
├── → Comunidade (card de build / navbar)
└── → Login (botão navbar)
    └── → Dashboard (pós-login)

PC Builder
├── → Página de Peça (clique em componente)
└── → Comunidade (publicar build)
```

---

## 5. Links de Design

| Recurso                      | Arquivo / Link                        | Status    |
|------------------------------|---------------------------------------|-----------|
| Wireframe Lo-Fi — Home Page  | `design/wireframe-home-lofi.html`     | Aprovado  |
| Hi-Fi — Home Page            | *(a gerar com prompt clean/laranja)*  | Pendente  |
| Wireframe — Login            | *(a criar)*                           | Pendente  |
| Wireframe — PC Builder       | *(a criar)*                           | Pendente  |

---

## 6. Decisões de Design Registradas

| Data       | Decisão                                           | Motivo                                              |
|------------|---------------------------------------------------|-----------------------------------------------------|
| 2026-05-18 | Escolha do estilo clean/moderno com laranja       | Mais familiar ao público BR (estilo KaBuM!/meupc.net), maior confiança e conversão |
| 2026-05-18 | Hi-Fi direto (sem wireframe lo-fi primeiro)       | Portfólio visual, Guilherme quer apresentação final |
| 2026-05-18 | Uso do Claude Design para prototipação inicial    | Mais agilidade na iteração de layout da home page   |

---

## 7. Próximos Passos

1. [ ] Finalizar e aprovar design da Home Page no Claude Design
2. [ ] Adicionar link do design aprovado na seção 5
3. [ ] Criar tela de Login
4. [ ] Criar tela do PC Builder
5. [ ] Definir componentes reutilizáveis no Figma (Design System)
