# Generated by Django 2.0.1 on 2020-07-24 17:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0027_cart_shipping_total'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cartitem',
            options={'ordering': ['-timestamp', '-updated']},
        ),
    ]
