# Generated by Django 3.2 on 2023-11-12 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watches', '0004_auto_20231112_1352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('processing', 'Processing'), ('shipping', 'Shipping'), ('delivered', 'Delivered')], default='pending', max_length=20),
        ),
    ]
