# Generated by Django 2.0.1 on 2019-06-28 09:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0019_auto_20190628_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_description',
            name='email',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
