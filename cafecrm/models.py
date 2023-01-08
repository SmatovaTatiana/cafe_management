import uuid
from django.db import models
from django.urls import reverse


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
        return reverse('cafecrm:product_detail',
                       args=[self.slug, ])


class Drink(models.Model):
    drink_name = models.CharField(max_length=50)

    class Meta:
        ordering = ('drink_name',)
        verbose_name = 'Drink'
        verbose_name_plural = 'Drinks'

    def __str__(self):
        return 'Order {}'.format(self.drink_name)

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
        return '{}'.format(self.drink)
