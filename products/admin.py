from django.contrib import admin
from .models import Product, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_name')
    search_fields = ('name', 'display_name')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'rating')
    list_filter = ('category',)  # ✅ comma makes it a tuple
    search_fields = ('name', 'sku', 'description')
    ordering = ('name',)          # ✅ comma makes it a tuple