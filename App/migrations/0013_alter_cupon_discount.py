# Generated by Django 4.2 on 2023-04-26 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0012_cupon_order_cupon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cupon',
            name='discount',
            field=models.DecimalField(decimal_places=2, max_digits=4),
        ),
    ]
