# Generated by Django 4.2.4 on 2023-11-20 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_product_detail'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sales_price',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
