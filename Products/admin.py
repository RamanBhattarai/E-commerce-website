from django.contrib import admin
from .models import Category, Product, ProductDescription


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image_display', 'product_count')
    search_fields = ('name',)
    readonly_fields = ('product_count',)

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = "Number of Products"

    def image_display(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="50" height="50" style="object-fit: cover;" />'
        return "No Image"
    image_display.allow_tags = True
    image_display.short_description = "Image"
    image_display.admin_order_field = "image"


class ProductDescriptionInline(admin.TabularInline):
    model = ProductDescription
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'brand', 'price', 'stock_count', 'status', 'category', 'created_at')
    list_filter = ('status', 'category', 'brand')
    search_fields = ('name', 'brand')
    ordering = ('-created_at',)
    inlines = [ProductDescriptionInline]


@admin.register(ProductDescription)
class ProductDescriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'key', 'value')
    list_filter = ('key',)
    search_fields = ('product__name', 'key', 'value')
