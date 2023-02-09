# Generated by Django 4.1.4 on 2023-01-28 15:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cafecrm', '0038_remove_selling_username_remove_sellingitem_username_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='selling',
            name='author',
        ),
        migrations.AddField(
            model_name='document',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Исполнитель'),
        ),
        migrations.AddField(
            model_name='selling',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Исполнитель'),
        ),
        migrations.AlterField(
            model_name='document',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Создано'),
        ),
        migrations.AlterField(
            model_name='document',
            name='description',
            field=models.TextField(blank=True, verbose_name='Комментарий'),
        ),
        migrations.AlterField(
            model_name='document',
            name='document_type',
            field=models.CharField(choices=[('Receipt', 'Receipt'), ('Consumption', 'Consumption')], max_length=20, verbose_name='Тип документа'),
        ),
        migrations.AlterField(
            model_name='documentitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='document_items', to='cafecrm.products', verbose_name='Товар'),
        ),
        migrations.AlterField(
            model_name='documentitem',
            name='quantity',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='drink',
            name='drink_name',
            field=models.CharField(max_length=50, verbose_name='Название напитка'),
        ),
        migrations.AlterField(
            model_name='drinkitem',
            name='drink',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='cafecrm.drink', verbose_name='Название напитка'),
        ),
        migrations.AlterField(
            model_name='drinkitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='drink_items', to='cafecrm.products', verbose_name='Продукт'),
        ),
        migrations.AlterField(
            model_name='drinkitem',
            name='quantity',
            field=models.PositiveIntegerField(default=0, verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='products',
            name='description',
            field=models.TextField(blank=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='products',
            name='min_stock',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Минимальный остаток'),
        ),
        migrations.AlterField(
            model_name='products',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='products',
            name='stock',
            field=models.PositiveIntegerField(default=0, verbose_name='Остаток'),
        ),
        migrations.AlterField(
            model_name='selling',
            name='comments',
            field=models.TextField(blank=True, verbose_name='Комментарий'),
        ),
        migrations.AlterField(
            model_name='selling',
            name='date',
            field=models.DateField(auto_now_add=True, verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='sellingitem',
            name='drink',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cafecrm.drink', verbose_name='Напиток'),
        ),
        migrations.AlterField(
            model_name='sellingitem',
            name='quantity',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='sellingitem',
            name='selling',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cafecrm.selling', verbose_name='Дата'),
        ),
    ]