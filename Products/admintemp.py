from django.contrib import admin
from .models import Product, ProductDescription, Category

# Register your models here.
class ProductDescriptionInline(admin.TabularInline):
    model = ProductDescription
    extra = 1  # how many empty description forms to show

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'price', 'stock_count', 'status', 'created_at')
    inlines = [ProductDescriptionInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
