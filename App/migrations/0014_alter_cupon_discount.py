# Generated by Django 4.2 on 2023-04-26 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0013_alter_cupon_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cupon',
            name='discount',
            field=models.IntegerField(),
        ),
    ]
