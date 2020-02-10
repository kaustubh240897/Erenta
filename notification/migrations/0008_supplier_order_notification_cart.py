# Generated by Django 2.0.1 on 2020-02-09 13:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0020_coupon_amount'),
        ('notification', '0007_auto_20200209_1826'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier_order_notification',
            name='cart',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='carts.Cart'),
        ),
    ]
