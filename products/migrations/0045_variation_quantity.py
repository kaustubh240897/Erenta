# Generated by Django 2.0.1 on 2020-02-03 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0044_auto_20200203_1109'),
    ]

    operations = [
        migrations.AddField(
            model_name='variation',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
