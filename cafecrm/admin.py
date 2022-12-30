from django.contrib import admin
from .models import *


@admin.register(Products)
class GoodsAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'unit', 'product_type']


class DrinkRecipesInline(admin.TabularInline):
    model = DrinkItems
    raw_id_fields = ['ingredient']


class DrinksAdmin(admin.ModelAdmin):
    list_display = ['drink_name', ]
    inlines = [DrinkRecipesInline]

admin.site.register(Drinks, DrinksAdmin)



