# Generated by Django 2.0.1 on 2019-06-27 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_supplier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplier',
            name='Shop_name',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]