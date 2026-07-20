# Estratégia de Testes - Hardware Tracker

**Status:** Planejamento  
**Última Atualização:** 2026-05-15  
**Versão:** 0.1 (Draft)

---

## 1. Visão Geral da Estratégia

Este documento define a abordagem de testes para o Hardware Tracker, cobrindo todas as camadas:
- **Testes Unitários** — Lógica de negócio isolada
- **Testes de Integração** — APIs e banco de dados
- **Testes E2E** — Fluxos de usuário completos
- **Testes de Performance** — Carga, latência
- **Testes de Segurança** — OWASP, autenticação

---

## 2. Pirâmide de Testes

```
        ╱╲
       ╱  ╲          E2E (5%)
      ╱────╲         - Selenium
     ╱      ╲        - Critical user flows
    ╱────────╲
   ╱          ╲      Integration (25%)
  ╱            ╲     - API tests
 ╱──────────────╲    - Database tests
╱               ╲   - Mock external APIs
╱_________________╲
                    Unit (70%)
                    - Lógica de negócio
                    - Utilitários
                    - Validações
```

---

## 3. Testes Unitários (Backend)

### 3.1 Framework

- **pytest** — Framework principal
- **pytest-django** — Plugin Django
- **unittest.mock** — Mocks e patches
- **factory-boy** — Factory para fixtures

### 3.2 Estrutura

```
backend/
└── tests/
    ├── __init__.py
    ├── conftest.py              # Fixtures globais
    ├── test_auth/
    │   ├── test_login.py
    │   ├── test_register.py
    │   └── test_token_refresh.py
    ├── test_hardware/
    │   ├── test_price_scraping.py
    │   ├── test_price_calculator.py
    │   └── test_hardware_search.py
    ├── test_builds/
    │   ├── test_build_creation.py
    │   ├── test_compatibility_check.py
    │   └── test_build_list.py
    ├── test_ai_service/
    │   ├── test_suggestions.py
    │   └── test_rag_integration.py
    └── fixtures/
        ├── users.py
        ├── hardware.py
        └── builds.py
```

### 3.3 Exemplo de Teste Unitário

```python
# test_hardware/test_price_calculator.py
import pytest
from decimal import Decimal
from hardware.services import PriceCalculator

@pytest.fixture
def price_calculator():
    return PriceCalculator()

def test_calculate_average_price(price_calculator):
    prices = [
        Decimal("1000.00"),
        Decimal("1200.00"),
        Decimal("800.00"),
    ]
    result = price_calculator.average(prices)
    assert result == Decimal("1000.00")

def test_apply_discount(price_calculator):
    original_price = Decimal("1000.00")
    discounted = price_calculator.apply_discount(original_price, 10)  # 10%
    assert discounted == Decimal("900.00")

@pytest.mark.parametrize("price,discount,expected", [
    (Decimal("1000"), 10, Decimal("900")),
    (Decimal("2000"), 15, Decimal("1700")),
    (Decimal("500"), 5, Decimal("475")),
])
def test_apply_discount_parametrized(price_calculator, price, discount, expected):
    result = price_calculator.apply_discount(price, discount)
    assert result == expected
```

### 3.4 Cobertura de Testes

- **Objetivo:** Mínimo 80% de cobertura
- **Ferramentas:**
  - `pytest-cov` para relatórios
  - CI/CD checará cobertura antes de merge

```bash
pytest --cov=backend --cov-report=html
```

---

## 4. Testes de Integração (Backend)

### 4.1 Framework

- **pytest-django** — Testes com Django
- **responses** — Mock de HTTP requests
- **pytest-vcr** — Gravação de requisições HTTP

### 4.2 Testes de API

```python
# test_hardware/test_api.py
import pytest
from django.test import Client
from django.urls import reverse

@pytest.mark.django_db
class TestHardwareAPI:
    
    def setup_method(self):
        self.client = Client()
    
    def test_list_hardware_success(self, hardware_list):
        """GET /api/hardware/ retorna lista de peças"""
        response = self.client.get(reverse('api:hardware-list'))
        assert response.status_code == 200
        assert len(response.json()) == 3
    
    def test_filter_by_category(self, hardware_list):
        """GET /api/hardware/?category=gpu filtra por categoria"""
        response = self.client.get(
            reverse('api:hardware-list'),
            {'category': 'gpu'}
        )
        assert response.status_code == 200
        assert all(h['category'] == 'gpu' for h in response.json())
    
    def test_search_hardware(self, hardware_list):
        """GET /api/hardware/?search=rtx busca por nome"""
        response = self.client.get(
            reverse('api:hardware-list'),
            {'search': 'RTX'}
        )
        assert response.status_code == 200
        assert len(response.json()) > 0
```

### 4.3 Testes com Database

```python
# test_builds/test_build_creation.py
@pytest.mark.django_db
def test_create_build_with_components(user, hardware_list):
    """Criar build com componentes deve calcular preço total"""
    build = Build.objects.create(
        user=user,
        name="Meu PC Gamer"
    )
    
    gpu = hardware_list[0]
    cpu = hardware_list[1]
    
    BuildComponent.objects.create(build=build, hardware=gpu, quantity=1)
    BuildComponent.objects.create(build=build, hardware=cpu, quantity=1)
    
    total = build.calculate_total_price()
    assert total == gpu.current_price + cpu.current_price
```

---

## 5. Testes E2E (Frontend)

### 5.1 Framework

- **Selenium** — Automação de browser
- **Cypress** — Alternative moderno (considerar)
- **pytest-selenium** — Integração com pytest

### 5.2 Fluxos Críticos a Testar

| Fluxo | Cenário | Passo |
|-------|---------|-------|
| **Login** | Usuário novo se registra | 1. Acessar login; 2. Preencher formulário; 3. Confirmar email; 4. Logar |
| **Criação de Build** | Usuário cria build gamer | 1. Home > PC Builder; 2. Selecionar peças; 3. Verificar compatibilidade; 4. Salvar |
| **Comparação de Preços** | Ver melhor preço | 1. Buscar componente; 2. Ver preços por loja; 3. Clicar em oferta |
| **Modo Claro/Escuro** | Trocar tema | 1. Header > Toggle dark mode; 2. Verificar aplicação |

### 5.3 Exemplo de Teste E2E

```python
# tests/e2e/test_build_creation.py
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="function")
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_create_and_share_build(browser, live_server):
    """Fluxo: Criar build gamer e compartilhar"""
    browser.get(f"{live_server.url}/")
    
    # 1. Clicar em "PC Builder"
    pc_builder_btn = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "pc-builder-btn"))
    )
    pc_builder_btn.click()
    
    # 2. Selecionar processador
    cpu_dropdown = browser.find_element(By.ID, "cpu-select")
    cpu_dropdown.click()
    cpu_option = browser.find_element(By.XPATH, "//option[contains(text(), 'Ryzen 5')]")
    cpu_option.click()
    
    # 3. Adicionar à build
    add_btn = browser.find_element(By.ID, "add-to-build")
    add_btn.click()
    
    # 4. Verificar compatibilidade
    compat_check = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "compat-check-result"))
    )
    assert "compatível" in compat_check.text.lower()
    
    # 5. Salvar build
    save_btn = browser.find_element(By.ID, "save-build")
    save_btn.click()
    
    # 6. Verificar sucesso
    success_msg = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "success-message"))
    )
    assert "salva com sucesso" in success_msg.text.lower()
```

---

## 6. Testes de Segurança

### 6.1 Checklist OWASP Top 10

- [ ] **Injection (SQL/Command)** — Usar ORM (Django ORM previne)
- [ ] **Broken Auth** — Testes de password reset, session expiry
- [ ] **Sensitive Data** — HTTPS obrigatório, sem logs de senhas
- [ ] **XXE** — Limitar tamanho de XML
- [ ] **Broken Access Control** — Testar autorização em endpoints privados
- [ ] **Security Misconfiguration** — Revisar settings.py
- [ ] **XSS** — Sanitizar inputs, usar templating seguro
- [ ] **CSRF** — Django csrf_token ativado
- [ ] **Using Components with Known Vulnerabilities** — Auditar dependencies
- [ ] **Insufficient Logging** — Logar eventos de segurança

### 6.2 Exemplo de Teste de Segurança

```python
# test_security/test_auth.py
@pytest.mark.django_db
def test_cannot_access_other_users_builds(authenticated_user, other_user):
    """Usuário não pode editar builds de outro usuário"""
    build = Build.objects.create(user=other_user, name="Build Privada")
    
    # Tentar editar com usuário autenticado diferente
    response = client.patch(
        reverse('api:build-detail', args=[build.id]),
        {'name': 'Alterado'},
        HTTP_AUTHORIZATION=f'Bearer {authenticated_user.token}'
    )
    
    assert response.status_code == 403  # Forbidden

def test_sql_injection_prevention():
    """Verificar que SQL injection não funciona"""
    malicious_query = "'; DROP TABLE hardware; --"
    
    # Não deve retornar erro de SQL, mas busca válida ou vazio
    response = client.get(
        reverse('api:hardware-list'),
        {'search': malicious_query}
    )
    
    # Verifica que tabela ainda existe
    assert Hardware.objects.count() > 0
```

---

## 7. Testes de Performance

### 7.1 Ferramentas

- **Django Debug Toolbar** — Análise de queries
- **Locust** — Teste de carga
- **Apache Bench** — Benchmark simples

### 7.2 Métricas Alvo

| Operação | Tempo Alvo | Limite |
|----------|-----------|--------|
| GET /api/hardware/ | < 200ms | 500ms |
| POST /api/builds/ | < 300ms | 700ms |
| GET /api/builds/{id}/compatibility/ | < 150ms | 400ms |
| Scraping de preços | < 5min | 10min |

### 7.3 Teste de Carga

```python
# tests/performance/locustfile.py
from locust import HttpUser, task

class HardwareTrackerUser(HttpUser):
    wait_time = 1
    
    @task(3)
    def list_hardware(self):
        self.client.get("/api/hardware/")
    
    @task(2)
    def search_hardware(self):
        self.client.get("/api/hardware/?search=gpu")
    
    @task(1)
    def get_build(self):
        self.client.get("/api/builds/1/")

# Executar: locust -f locustfile.py -u 100 -r 10 --run-time 5m
```

---

## 8. Testes Manuais (QA)

### 8.1 Checklist de Regressão

- [ ] Home page carrega corretamente
- [ ] Modo claro/escuro funciona
- [ ] Responsividade em mobile/tablet
- [ ] Login funciona
- [ ] Busca de hardware filtra corretamente
- [ ] Criação de build salva
- [ ] Compatibilidade verifica corretamente
- [ ] Preços são exibidos por loja
- [ ] Newsletter captura email
- [ ] Links de redes sociais funcionam

---

## 9. CI/CD (GitHub Actions)

### 9.1 Configuração

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_DB: hardware_tracker_test
          POSTGRES_PASSWORD: test
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.10
      
      - name: Install dependencies
        run: |
          pip install -r requirements-test.txt
      
      - name: Run tests
        run: |
          pytest --cov=backend --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

---

## 10. Próximos Passos

1. [ ] Configurar pytest e pytest-django
2. [ ] Criar fixtures globais (conftest.py)
3. [ ] Implementar testes unitários do auth
4. [ ] Implementar testes de API
5. [ ] Configurar Selenium para E2E
6. [ ] Implementar teste de segurança básica
7. [ ] Configurar CI/CD com GitHub Actions
8. [ ] Documentar procedimento manual QA

---

## 11. Referências

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-django](https://pytest-django.readthedocs.io/)
- [Django Testing](https://docs.djangoproject.com/en/stable/topics/testing/)
- [Selenium Documentation](https://www.selenium.dev/documentation/)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [GitHub Actions CI/CD](https://docs.github.com/en/actions)
