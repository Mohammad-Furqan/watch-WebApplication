# Generated by Django 3.2 on 2023-12-07 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watches', '0006_auto_20231114_1139'),
    ]

    operations = [
        migrations.AddField(
            model_name='watch',
            name='stock_quantity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]