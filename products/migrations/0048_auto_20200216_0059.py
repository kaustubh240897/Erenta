# Generated by Django 2.0.1 on 2020-02-15 19:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0047_auto_20200216_0003'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productimage',
            old_name='product_name',
            new_name='product',
        ),
    ]
