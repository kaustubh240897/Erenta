# Generated by Django 2.0.1 on 2019-06-22 09:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20190622_0002'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order_details',
            name='billing_profile',
        ),
        migrations.AddField(
            model_name='order_details',
            name='order_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.Order'),
        ),
    ]