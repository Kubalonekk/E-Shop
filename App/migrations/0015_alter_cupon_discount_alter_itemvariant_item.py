# Generated by Django 4.2 on 2023-04-27 10:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0014_alter_cupon_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cupon',
            name='discount',
            field=models.IntegerField(help_text='Wartość procentowa kuponu'),
        ),
        migrations.AlterField(
            model_name='itemvariant',
            name='item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item_variant', to='App.item'),
        ),
    ]