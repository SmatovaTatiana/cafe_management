# Generated by Django 4.1.4 on 2023-01-10 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafecrm', '0032_selling_sellingitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='selling',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
