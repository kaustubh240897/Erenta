# Generated by Django 2.0.1 on 2019-05-27 07:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_product_description_featured'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product_description',
            old_name='featured',
            new_name='active',
        ),
    ]
