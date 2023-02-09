# Generated by Django 4.1.4 on 2023-01-27 15:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cafecrm', '0037_sellingitem_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='selling',
            name='username',
        ),
        migrations.RemoveField(
            model_name='sellingitem',
            name='username',
        ),
        migrations.AddField(
            model_name='selling',
            name='author',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]