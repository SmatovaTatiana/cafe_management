from django.db import models
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
class Goods(BaseDataModel):
    PRODUCT = 'product'
    TARE = 'tare'
    SNACK = 'snack'

    GOOD_CATEGORY = (
        (PRODUCT, 'Продукт'),
        (TARE, 'Тара'),
        (SNACK, 'Штучный товар')
    )

    PC = 'pc'
    ML = 'ml'
    GR = 'gr'

    UNITS = (
        (PC, 'шт.'),
        (ML, 'мл'),
        (GR, 'гр')
    )

    title = models.CharField(max_length=250, verbose_name='Наименование')
    unit = models.CharField(max_length=20, choices=UNITS, verbose_name='Единица измерения')
    category = models.CharField(max_length=20, choices=GOOD_CATEGORY, verbose_name='Категория')

    def __str__(self):
        return '{title}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['title']


class Operations(models.Model):
    username = models.CharField(max_length=200, verbose_name='Пользователь', null=True, blank=True)
    operation = models.TextField(verbose_name='Операция')
    create_date = models.DateTimeField(verbose_name='Дата и время операции', default=timezone.now)

    class Meta:
        verbose_name = 'Операция'
        verbose_name_plural = 'Операции'
        ordering = ['-create_date']


# Напитки / Drinks (cafe menu)
class Drinks(BaseDataModel):
    drink_name = models.CharField(max_length=100, verbose_name='Название напитка')

    def __str__(self):
        return f'{self.drink_name}'

    class Meta:
        verbose_name = 'Напиток'
        verbose_name_plural = 'Напитки'
        ordering = ['drink_name']


# recipe / рецепт
class DrinkRecipes(models.Model):
    drink_name = models.ForeignKey(Drinks, on_delete=models.CASCADE, verbose_name='Напиток')
    ingredient = models.ForeignKey(Goods, on_delete=models.PROTECT, verbose_name='Продукт')
    quantity = models.IntegerField(verbose_name='Количество')

    def __str__(self):
        return f'{self.ingredient.title}. Количество {self.quantity}'

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


# documents (income and expense). Документы (приход - расход)
class Documents(BaseDataModel):
    INCOME = 'income'
    EXPENSE = 'expense'

    DOCUMENT_TYPE = (
        (INCOME, 'Приход'),
        (EXPENSE, 'Расход')
    )

    document_type = models.CharField(max_length=10, choices=DOCUMENT_TYPE, verbose_name='Тип документа')
    apply_flag = models.BooleanField(verbose_name='Документ проведен', default=False)

    def __str__(self):
        return f'{self.pk} от: {str(self.create_date)[:19]}'

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'
        ordering = ['-create_date']


class DocumentItems(models.Model):
    document = models.ForeignKey(Documents, on_delete=models.CASCADE, verbose_name='Документ')
    good = models.ForeignKey(Goods, on_delete=models.PROTECT, verbose_name='Товар')
    count = models.IntegerField(verbose_name='Количество')

    def __str__(self):
        return f'{self.good.title}. Количество {self.count}'

    class Meta:
        verbose_name = 'Товар в документе'
        verbose_name_plural = 'Товары в документе'


# /остатки / storage
class StorageItems(BaseDataModel):
    item = models.OneToOneField(Goods, on_delete=models.PROTECT, verbose_name='Товар')
    count = models.IntegerField(verbose_name='Количество')

    def __str__(self):
        return f'{str(self.item)} ({self.count})'

    class Meta:
        verbose_name = 'Остаток'
        verbose_name_plural = 'Остатки'
