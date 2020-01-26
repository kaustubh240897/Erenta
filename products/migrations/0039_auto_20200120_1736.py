# Generated by Django 2.0.1 on 2020-01-20 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0038_variation_discount_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variation',
            name='discount_price',
        ),
        migrations.AddField(
            model_name='product_description',
            name='discount_price',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
