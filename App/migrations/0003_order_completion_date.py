# Generated by Django 4.2 on 2023-04-24 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0002_order_payment_in_progress'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='completion_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]