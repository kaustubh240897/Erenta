# Generated by Django 2.0.1 on 2020-05-21 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0063_auto_20200512_1809'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier_review',
            name='reviewed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user_review',
            name='reviewed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user_review',
            name='rating',
            field=models.IntegerField(default=5),
        ),
    ]
