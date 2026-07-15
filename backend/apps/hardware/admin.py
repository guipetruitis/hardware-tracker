from django.contrib import admin
from .models import Category, Hardware, Store, Price, PriceHistory

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'created_at')
    list_filter = ('created_at',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    ordering = ('order',)

@admin.register(Hardware)
class HardwareAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'manufacturer', 'model', 'sku', 'created_at', 'updated_at', 'deleted_at')
    list_filter = ('category', 'manufacturer', 'created_at', 'updated_at', 'deleted_at')
    search_fields = ('name', 'manufacturer', 'model', 'sku')
    ordering = ('name',)

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'url', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'slug')
    ordering = ('name',)

@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ('hardware', 'store', 'price', 'in_stock', 'scraped_at')
    list_filter = ('store', 'in_stock', 'scraped_at')

@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = ('hardware', 'store', 'price', 'status', 'currency', 'recorded_at')
    list_filter = ('store', 'status', 'recorded_at')