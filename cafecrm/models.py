import uuid

from django.db import models
from django.urls import reverse
from django.utils import timezone


# вспмогательная модель для фиксирования даты изменения состояния объектов
# additional model for fixing the date of changing the object states
class BaseDataModel(models.Model):
    create_date = models.DateTimeField(verbose_name='Дата создания', default=timezone.now)
    update_date = models.DateTimeField(verbose_name='Дата изменения', default=timezone.now)
    to_remove = models.BooleanField(verbose_name='Помечен на удаление', null=False, default=False)

    class Meta:
        abstract = True


# товары / goods
class Products(models.Model):
    PRODUCT = 'product'
    SNACK = 'snack'
    TARE = 'tare'
    PRODUCT_TYPE = ((PRODUCT, 'продукт'), (SNACK, 'штучный товар'), (TARE, 'тара'))

    PC = 'шт.'
    ML = 'мл'
    GR = 'гр'
    UNITS = ((PC, 'шт.'), (ML, 'мл'), (GR, 'гр'))

    product_name = models.CharField(max_length=250, verbose_name='Наименование')
    unit = models.CharField(max_length=20, choices=UNITS, verbose_name='Единица измерения')
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPE, verbose_name='Категория')
    slug = models.SlugField(max_length=200, db_index=True, unique='product_name', default=uuid.uuid4)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['product_name']
        index_together = (('id', 'slug'),)

    def __str__(self):
        return '{}'.format(self.product_name)

    def get_absolute_url(self):
        return reverse('product_detail',
                       args=[self.slug, ])


# Напитки / Drinks (cafe menu)
class Drinks(models.Model):
    drink_name = models.CharField(max_length=100, verbose_name='Название напитка')
    slug = models.SlugField(max_length=200, db_index=True, unique='drink_name', default=uuid.uuid4)

    def __str__(self):
        return '{}'.format(self.drink_name)

    class Meta:
        verbose_name = 'Напиток'
        verbose_name_plural = 'Напитки'
        ordering = ['drink_name']


# recipe / рецепт
class DrinkItems(models.Model):
    drink_name = models.ForeignKey(Drinks, on_delete=models.CASCADE, verbose_name='Напиток')
    ingredient = models.ForeignKey(Products, on_delete=models.PROTECT, verbose_name='Продукт')
    quantity = models.IntegerField(verbose_name='Количество', default=1)

    def __str__(self):
        return '{}'.format(self.id)

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
