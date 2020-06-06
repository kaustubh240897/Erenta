# Generated by Django 2.0.1 on 2020-05-17 17:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('carts', '0026_auto_20200508_1608'),
        ('products', '0063_auto_20200512_1809'),
        ('notification', '0011_auto_20200304_0036'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order_current_status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variations', models.CharField(default='None', max_length=50)),
                ('status', models.CharField(default='created', max_length=50)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('cart', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='carts.Cart')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.Product_description')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='order_notification',
            name='cart',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='carts.Cart'),
        ),
        migrations.AddField(
            model_name='order_notification',
            name='order_id',
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name='order_notification',
            name='status',
            field=models.CharField(default='created', max_length=120),
        ),
    ]