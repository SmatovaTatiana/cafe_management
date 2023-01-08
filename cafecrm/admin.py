from django.contrib import admin
from .models import Products, Drink, DrinkItem


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'unit', 'product_type', 'price', 'stock', 'slug']
    prepopulated_fields = {'slug': ('product_name', )}


class DrinkItemInline(admin.TabularInline):
    model = DrinkItem
    raw_id_fields = ['product']


class DrinkAdmin(admin.ModelAdmin):
    list_display = ['id', 'drink_name']
    inlines = [DrinkItemInline]


admin.site.register(Drink, DrinkAdmin)
