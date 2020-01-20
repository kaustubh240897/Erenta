# Generated by Django 2.0.1 on 2019-07-25 14:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_remove_supplier_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier',
            name='email',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]