from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode


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
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    stock = models.PositiveIntegerField(default=0)
    min_stock = models.PositiveSmallIntegerField(default=0)
    description = models.TextField(blank=True)
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
    drink_name = models.CharField(max_length=50)
    slug = models.SlugField(unique='drink_name', blank=True)

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
    drink = models.ForeignKey(Drink, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, related_name='drink_items', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return '{}'.format(self.product)


class Document(models.Model):
    RECEIPT = 'Receipt'
    CONSUMPTION = 'Consumption'
    DOCUMENT_TYPE = ((RECEIPT, 'Receipt'), (CONSUMPTION, 'Consumption'))

    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE, verbose_name='document type')
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Document {}'.format(self.id)


class DocumentItem(models.Model):
    document = models.ForeignKey(Document, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, related_name='document_items', on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return '{}'.format(self.id)


class Selling(models.Model):
    date = models.DateField(auto_now_add=True)
    comments = models.TextField(blank=True)

    class Meta:
        ordering = ('date',)

    def __str__(self):
        return 'Selling {}'.format(self.pk)


class SellingItem(models.Model):
    selling = models.ForeignKey(Selling, on_delete=models.CASCADE)
    drink = models.ForeignKey(Drink, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return '{}'.format(self.drink)
