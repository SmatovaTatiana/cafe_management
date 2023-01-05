from django.contrib import admin
from .models import *


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'unit', 'product_type', 'price', 'stock', 'slug']
    prepopulated_fields = {'slug': ('product_name', )}


class DrinkRecipesInline(admin.TabularInline):
    model = DrinkItems
    raw_id_fields = ['ingredient']


class DrinksAdmin(admin.ModelAdmin):
    list_display = ['drink_name', ]
    prepopulated_fields = {'slug': ('drink_name',)}
    inlines = [DrinkRecipesInline]

admin.site.register(Drinks, DrinksAdmin)



