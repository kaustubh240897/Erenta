# Generated by Django 2.1.7 on 2021-04-28 08:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0057_sub_category_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='sub_sub_category',
            name='sub_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.Sub_Category'),
        ),
    ]