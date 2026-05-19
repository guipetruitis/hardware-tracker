# Requisitos do Projeto - Hardware Tracker

**Status:** Levantamento Completo  
**Última Atualização:** 2026-05-15  
**Versão:** 1.0

---

## 1. Visão Geral

Hardware Tracker é uma plataforma brasileira de comparação de preços e montagem de computadores, inspirada no [meupc.net](https://meupc.net/).

**Objetivo:** Ajudar usuários a montar PCs customizados com verificação de compatibilidade e comparação de preços em tempo real.

---

## 2. Funcionalidades Principais

### 2.1 Core Features

- **Comparador de Preços**
  - Integração com lojas: Terabyte, Kabum, Amazon, Pichau
  - Agregação de preços em tempo real
  - Exibição do melhor preço entre lojas

- **Histórico de Preços**
  - Rastreamento de variação de preço por peça
  - Gráficos de histórico (últimos 30/60/90 dias)

- **Verificador de Compatibilidade**
  - Validação de compatibilidade entre componentes
  - Alertas de incompatibilidade
  - Sugestões de ajustes

- **Cupons e Ofertas**
  - Exibição de cupons disponíveis
  - Ofertas em destaque na home

### 2.2 PC Builder (Ferramenta de Montagem)

- **Criador de Build Interativo**
  - Interface drag-and-drop ou seleção por categoria
  - Verificação de compatibilidade em tempo real

- **IA Integrada**
  - Sugestões de peças baseadas em:
    - Requisitos do usuário (tipo de uso: gamer, produção, etc.)
    - Conhecimento extraído do Reddit via RAG
    - Modelos de LLM (Groq, Claude, Gemini)

- **Área de Pré-montados**
  - Sugestões de computadores já montados para compra
  - Filtrados por perfil de uso

- **Filtros Avançados**
  - Loja
  - Tipo de uso (Gamer, Produção, Office, etc.)
  - Fabricante (Intel, AMD, NVIDIA, etc.)
  - Faixa de preço
  - Capacidade (RAM, Armazenamento)

### 2.3 Comunidade

- **Builds Públicas**
  - Compartilhamento de builds criadas
  - Ranking de builds (recentes, populares, all-time)

- **Sistema de Comentários**
  - Sugestões de melhoria
  - Discussões na comunidade

- **Leaderboard**
  - Melhores builds do mês
  - Melhores builds de todos os tempos
  - Builds mais recentes

### 2.4 Distribuição (Futuro)

- **Extensão de Navegador**
  - Comparador de preços ao navegar sites (estilo Bilômetro)
  - Compatível com lojas de hardware

- **Bot no Telegram**
  - Alertas de ofertas em peças seguidas
  - Notificações de queda de preço

---

## 3. Componentes Suportados

### Hardware Principal
- Processadores (Intel, AMD)
- Coolers
- Placas de Vídeo (NVIDIA, AMD)
- Placas-Mãe
- Memória RAM
- Armazenamento (SSD, HDD)
- Fontes de Alimentação

### Periféricos
- Gabinetes
- Monitores
- Mouses
- Teclados
- Cadeiras
- Mousepads

---

## 4. Estrutura de Telas

### 4.1 Home Page

- **Hero Section**
  - Imagem atrativa + frase de impacto
  - Exemplos: "24.3k peças disponíveis"
  - Destaque para comparador e verificador

- **Seção Como Ajudamos**
  - Dicas de montagem
  - Destaque para sistema de teste de compatibilidade
  - Destaque para comparador de preços
  - Destaque para comunidade

- **Conteúdo Principal**
  - Ofertas em destaque
  - Builds recentes da comunidade

- **Estatísticas**
  - Total de testes de compatibilidade realizados
  - Total de builds criadas
  - Quantidade de peças em base de dados

- **Newsletter**
  - Campo de captura de email

### 4.2 Outras Telas

- **Login/Autenticação**
- **Tela de Build (criação/visualização)**
- **Tela de Peças (detalhes, histórico, cupons)**
- **Tela de Comunidade (ranking, comentários)**
- **Dashboard de Usuário (meus builds, preferências)**

### 4.3 Rodapé (Footer)

- SIGA-NOS (redes sociais)
- SOBRE
- MEUPC.NET (link para home)
- HARDWARE
- PERIFÉRICOS E OUTROS
- Logo
- Direitos Reservados

---

## 5. Requisitos de UI/UX

- **Responsividade**: Mobile, Tablet, Desktop
- **Temas**: Modo Claro (Light) e Modo Escuro (Dark)
- **Identidade Visual**
  - Logo customizado
  - Paleta de cores definida
  - Tipografia consistente
- **Acessibilidade**: WCAG 2.1 AA (objetivo)
- **Performance**: Carregamento rápido, otimização de imagens

---

## 6. Lojas e Integrações

### 6.1 Lojas de Hardware

| Loja | Link | Status |
|------|------|--------|
| TerabyteShop | https://www.terabyteshop.com.br/ | Planejado |
| KaBuM! | https://www.kabum.com.br/ | Planejado |
| Amazon Brasil | https://www.amazon.com.br/ | Planejado |
| Pichau | https://www.pichau.com.br/ | Planejado |

### 6.2 Integrações de IA

- **Groq SDK**: Inferência rápida de LLMs
- **Claude API**: Processamento de texto e recomendações
- **Gemini API**: Análise de imagens e dados
- **n8n**: Orquestração de workflows
- **RAG (Retrieval-Augmented Generation)**: Busca de conhecimento em Reddit

---

## 7. Critérios de Aceitação

### MVP (Minimum Viable Product)

- [ ] Comparador de preços funcional (2+ lojas)
- [ ] Verificador de compatibilidade básico
- [ ] Home page com design responsivo
- [ ] Login de usuário (email/senha)
- [ ] Criação de builds simples
- [ ] Exibição de builds da comunidade
- [ ] Newsletter funcional

### Post-MVP

- [ ] IA integrada com sugestões
- [ ] Histórico de preços com gráficos
- [ ] Extensão de navegador
- [ ] Bot Telegram
- [ ] Sistema de comentários robusto

---

## 8. Priorização de Features

| Feature | Prioridade | Sprint | Complexidade |
|---------|-----------|--------|--------------|
| Home page + protótipo UI | **Alta** | Sprint 1 | Média |
| Comparador de preços (scraping) | **Alta** | Sprint 1-2 | Alta |
| Autenticação | **Alta** | Sprint 2 | Média |
| PC Builder básico | **Alta** | Sprint 2-3 | Alta |
| Verificador de compatibilidade | **Alta** | Sprint 3 | Alta |
| Comunidade (builds públicas) | **Média** | Sprint 4 | Média |
| IA (sugestões) | **Média** | Sprint 4-5 | Muito Alta |
| Histórico de preços | **Média** | Sprint 5 | Média |
| Bot Telegram | **Baixa** | Sprint 6+ | Média |
| Extensão de navegador | **Baixa** | Sprint 6+ | Muito Alta |

---

## 9. Referências

- [meupc.net](https://meupc.net/) — Referência visual e funcional principal
- [YouTube: Como Montar um PC Gamer](https://www.youtube.com/watch?v=8ZNtz09sQlk) — Caso de uso
- [Portfólio do Allan](https://portfolio-henna-pi-77.vercel.app/) — Inspiração tecnológica

---

## 10. Próximos Passos

1. [ ] Validar requisitos com stakeholders (se aplicável)
2. [ ] Criar wireframes no Figma
3. [ ] Definir modelo de dados (DATABASE.md)
4. [ ] Planejar arquitetura (ARCHITECTURE.md)
5. [ ] Iniciar desenvolvimento de protótipo
