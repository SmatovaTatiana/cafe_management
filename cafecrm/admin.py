from django.contrib import admin
from .models import Products, Drink, DrinkItem, Document, DocumentItem, Selling, SellingItem


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_name', 'unit', 'product_type', 'stock', 'min_stock', 'need_to_order']
    prepopulated_fields = {'slug': ('product_name', )}
    ordering = ['product_type']



class DrinkItemInline(admin.TabularInline):
    model = DrinkItem
    raw_id_fields = ['product']


class DrinkAdmin(admin.ModelAdmin):
    list_display = ['id', 'drink_name']
    prepopulated_fields = {'slug': ('drink_name', )}
    inlines = [DrinkItemInline]


admin.site.register(Drink, DrinkAdmin)


class DocumentItemInline(admin.TabularInline):
    model = DocumentItem
    raw_id_fields = ['product']


class DocumentAdmin(admin.ModelAdmin):
    list_display = ['id', 'created', 'created_by', 'document_type']
    inlines = [DocumentItemInline]


admin.site.register(Document, DocumentAdmin)


class SellingItemInline(admin.TabularInline):
    model = SellingItem
    raw_id_fields = ['drink']


class SellingAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'created_by', 'comments']
    inlines = [SellingItemInline]



admin.site.register(Selling, SellingAdmin)