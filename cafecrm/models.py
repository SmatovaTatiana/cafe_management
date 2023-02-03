from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode


# Продукты, товары
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
    slug = models.SlugField(max_length=200, db_index=True, unique='product_name')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Цена', blank=True, null=True)
    stock = models.PositiveIntegerField(default=0, verbose_name='Остаток', blank=True, null=True)
    min_stock = models.PositiveSmallIntegerField(default=0, verbose_name='Минимальный остаток', blank=True, null=True)
    description = models.TextField(blank=True, verbose_name='Описание')
    need_to_order = property(
        lambda self: (self.min_stock - self.stock if self.stock < self.min_stock else 0)
        )

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['product_type', 'product_name']
        index_together = (('id', 'slug'),)

    def __str__(self):
        return '{}'.format(self.product_name)

    def get_absolute_url(self):
        return reverse('cafecrm:product_detail', args=[self.slug, ])

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(unidecode(self.product_name))
        return super().save(*args, **kwargs)


class Drink(models.Model):
    DRINK = 'drink'
    SNACK = 'snack'
    MENU_TYPE = ((DRINK, 'напиток'), (SNACK, 'штучный товар'))

    drink_name = models.CharField(max_length=50, verbose_name='Название')
    slug = models.SlugField(unique='drink_name', blank=True)
    menu_type = models.CharField(max_length=20, choices=MENU_TYPE, verbose_name='Категория')

    class Meta:
        ordering = ('drink_name',)
        verbose_name = 'Drink'
        verbose_name_plural = 'Drinks'

    def save(self, *args, **kwargs):  # save slug from form
        if not self.slug:
            self.slug = slugify(unidecode(self.drink_name))
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('cafecrm:drink_detail', args=[self.slug, ])

    def __str__(self):
        return '{}'.format(self.drink_name)

    @classmethod
    def get_or_none(cls, **kwargs):
        try:
            return cls.objects.get(**kwargs)
        except cls.DoesNotExist:
            return None


class DrinkItem(models.Model):
    drink = models.ForeignKey(Drink, related_name='items', on_delete=models.CASCADE, verbose_name='Название')
    product = models.ForeignKey(Products, related_name='drink_items', on_delete=models.PROTECT, verbose_name='Продукт')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')

    def __str__(self):
        return '{}'.format(self.product)


class Document(models.Model):
    RECEIPT = 'Приход'
    CONSUMPTION = 'Расход'
    DOCUMENT_TYPE = ((RECEIPT, 'Приход'), (CONSUMPTION, 'Расход'))

    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE, verbose_name='Тип документа')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Исполнитель')
    description = models.TextField(blank=True, verbose_name='Комментарий')

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Document {}'.format(self.id)


class DocumentItem(models.Model):
    document = models.ForeignKey(Document, related_name='items', on_delete=models.CASCADE, verbose_name='Документ')
    product = models.ForeignKey(Products, related_name='document_items', on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Количество')

    def __str__(self):
        return '{}'.format(self.id)


class Selling(models.Model):
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    comments = models.TextField(blank=True, verbose_name='Комментарий')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Исполнитель')

    class Meta:
        ordering = ('date',)

    def __str__(self):
        return 'Selling {}'.format(self.pk)


class SellingItem(models.Model):
    selling = models.ForeignKey(Selling, on_delete=models.CASCADE, verbose_name='Дата')
    drink = models.ForeignKey(Drink, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Количество')

    def __str__(self):
        return '{}'.format(self.drink)
