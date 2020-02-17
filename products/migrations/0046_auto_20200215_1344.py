# Generated by Django 2.0.1 on 2020-02-15 08:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0045_variation_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quantity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('active', models.BooleanField(default=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product_description')),
            ],
        ),
        migrations.RemoveField(
            model_name='variation',
            name='quantity',
        ),
        migrations.AddField(
            model_name='quantity',
            name='variations',
            field=models.ManyToManyField(blank=True, to='products.Variation'),
        ),
    ]
