# Generated by Django 2.0.1 on 2021-02-19 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0010_auto_20210219_1521'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='supplier_cancellation',
            field=models.BooleanField(default=False),
        ),
    ]
