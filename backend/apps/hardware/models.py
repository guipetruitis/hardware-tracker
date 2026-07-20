from django.db import models

class Category(models.Model):
    """Categoria de componente (ex: Processador, Placa de Vídeo, RAM).

    Usada para agrupar e filtrar hardwares no catálogo. O campo `order`
    controla a ordem de exibição no menu e nos filtros do site.
    """

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    icon_url = models.URLField(max_length=500, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']     # ordena os registros por 'order' por padrão

    def __str__(self):
        return self.name

class Hardware(models.Model):
    """Componente de PC cadastrado no sistema.

    Representa uma peça física (CPU, GPU, RAM, etc.). Os dados técnicos
    variáveis por categoria (socket, TDP, VRAM...) ficam em `specifications`
    como JSONB, evitando dezenas de colunas nulas.

    O campo `deleted_at` implementa soft delete — a peça não é removida do
    banco, apenas marcada como inativa, preservando histórico de preços e builds.
    """

    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='hardware')
    manufacturer = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)
    sku = models.CharField(max_length=100, blank=True, null=True)
    specifications = models.JSONField(blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta: 
        ordering = ['-created_at']  # ordena os registros por 'created_at' em ordem decrescente por padrão
    def __str__(self):
        return self.name

class Store(models.Model):
    """Loja de e-commerce cadastrada no sistema.

    Cada loja tem um catálogo próprio de hardwares, com preços e disponibilidade
    que variam diariamente. O campo `is_active` permite desativar lojas sem
    removê-las do banco, preservando histórico de preços.
    """

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    url = models.URLField(max_length=500, blank=True, null=True)
    logo_url = models.URLField(max_length=500, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class Price(models.Model):
    """Preço de um hardware em uma loja específica.

    Registra o preço atual, disponibilidade e URL do produto.
    A combinação `hardware` e `store` deve ser única.
    """
    hardware = models.ForeignKey(Hardware, on_delete=models.PROTECT, related_name='prices')
    store = models.ForeignKey('Store', on_delete=models.PROTECT, related_name='prices')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    in_stock = models.BooleanField(default=True)
    product_url = models.URLField(max_length=500, blank=True, null=True)
    scraped_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ── (regras/config sobre a tabela) ──
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['hardware', 'store'],
                name='unique_price_per_hardware_store'
            )
        ]
    
    def __str__(self):
        return f"{self.hardware.name} - {self.store.name} - {self.price} ({'In Stock' if self.in_stock else 'Out of Stock'})"

class PriceHistory(models.Model):
    """Histórico de preços de um hardware em uma loja específica.

    Cada registro representa o preço e disponibilidade de um hardware em uma
    loja em um determinado dia. O campo `status` indica se o hardware estava
    disponível ou indisponível naquele momento.
    """

    hardware = models.ForeignKey(Hardware, on_delete=models.PROTECT, related_name='price_history')
    store = models.ForeignKey(Store, on_delete=models.PROTECT, related_name='price_history')
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20, default='available')  # 'available' | 'unavailable'
    currency = models.CharField(max_length=3, default='BRL')
    recorded_at = models.DateTimeField(auto_now_add=True)
