# Generated by Django 2.0.1 on 2019-06-17 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0002_auto_20190607_1354'),
    ]

    operations = [
        migrations.AddField(
            model_name='billingprofile',
            name='customer_id',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
