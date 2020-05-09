# Generated by Django 2.0.1 on 2020-05-08 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0025_cartitem_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='cancel_granted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='cancel_request',
            field=models.BooleanField(default=False),
        ),
    ]
