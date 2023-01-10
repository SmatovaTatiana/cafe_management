# Generated by Django 4.1.4 on 2023-01-05 17:52

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cafecrm', '0020_alter_drinks_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='slug',
            field=models.SlugField(default=uuid.uuid1, max_length=200, unique='product_name'),
        ),
    ]