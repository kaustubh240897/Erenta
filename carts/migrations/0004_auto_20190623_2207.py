# Generated by Django 2.0.1 on 2019-06-23 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0003_auto_20190623_2203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='size',
            field=models.CharField(default=None, max_length=10),
        ),
    ]
