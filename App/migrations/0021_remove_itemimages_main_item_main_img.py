# Generated by Django 4.2 on 2023-05-24 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0020_cupon_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemimages',
            name='main',
        ),
        migrations.AddField(
            model_name='item',
            name='main_img',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
