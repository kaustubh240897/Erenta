# Generated by Django 2.0.1 on 2020-01-11 17:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0034_productimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Variation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('active', models.BooleanField(default=False)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.ProductImage')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='product_description',
            unique_together={('product_name', 'slug')},
        ),
        migrations.AddField(
            model_name='variation',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product_description'),
        ),
    ]
