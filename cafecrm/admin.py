from django.contrib import admin
from .models import Products, Drink, DrinkItem, Document, DocumentItem


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_name', 'unit', 'product_type', 'price', 'stock', 'slug']
    prepopulated_fields = {'slug': ('product_name', )}
    ordering = ['product_type']


class DrinkItemInline(admin.TabularInline):
    model = DrinkItem
    raw_id_fields = ['product']


class DrinkAdmin(admin.ModelAdmin):
    list_display = ['id', 'drink_name', 'slug']
    prepopulated_fields = {'slug': ('drink_name', )}
    inlines = [DrinkItemInline]


admin.site.register(Drink, DrinkAdmin)


class DocumentItemInline(admin.TabularInline):
    model = DocumentItem
    raw_id_fields = ['product']


class DocumentAdmin(admin.ModelAdmin):
    list_display = ['id', 'document_type', 'created']
    inlines = [DocumentItemInline]


admin.site.register(Document, DocumentAdmin)
