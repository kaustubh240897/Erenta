# Generated by Django 2.0.1 on 2021-02-17 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0008_transactionmessage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transactionmessage',
            name='cartitem',
        ),
        migrations.AddField(
            model_name='transactionmessage',
            name='cart_id',
            field=models.CharField(blank=True, max_length=120),
        ),
    ]