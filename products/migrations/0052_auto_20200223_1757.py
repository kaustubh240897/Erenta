# Generated by Django 2.0.1 on 2020-02-23 12:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0051_auto_20200221_1335'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quantity',
            name='product',
        ),
        migrations.RemoveField(
            model_name='quantity',
            name='variations',
        ),
        migrations.DeleteModel(
            name='Quantity',
        ),
    ]
