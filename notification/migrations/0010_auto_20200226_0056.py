# Generated by Django 2.0.1 on 2020-02-25 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0009_auto_20200226_0036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='low_quantity_notification',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]