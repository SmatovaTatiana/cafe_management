# Generated by Django 4.1.4 on 2023-01-05 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafecrm', '0014_products_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='slug',
            field=models.SlugField(default='name', max_length=200),
        ),
    ]
