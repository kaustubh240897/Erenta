# Generated by Django 2.0.1 on 2019-05-27 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_product_description_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_description',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]