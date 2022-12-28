from django.contrib import admin
from .models import *


@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit', 'category']


@admin.register(Operations)
class OperationsAdmin(admin.ModelAdmin):
    list_display = ['username', 'operation', 'create_date']


@admin.register(Drinks)
class DrinksAdmin(admin.ModelAdmin):
    list_display = ['drink_name']


@admin.register(DrinkRecipes)
class DrinkRecipesAdmin(admin.ModelAdmin):
    list_display = ['drink_name', 'ingredient', 'quantity']


@admin.register(Documents)
class DocumentsAdmin(admin.ModelAdmin):
    list_display = ['id', 'document_type', 'apply_flag', 'create_date', 'update_date', 'to_remove']


@admin.register(DocumentItems)
class DocumentItemsAdmin(admin.ModelAdmin):
    list_display = ['document', 'good', 'count']


@admin.register(StorageItems)
class StorageItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'item', 'count', 'to_remove']
