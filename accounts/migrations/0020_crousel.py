# Generated by Django 2.1.7 on 2021-04-19 12:01

import accounts.models
from django.db import migrations, models
import stdimage.validators


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_auto_20200726_1753'),
    ]

    operations = [
        migrations.CreateModel(
            name='Crousel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=accounts.models.upload_image_path, validators=[stdimage.validators.MaxSizeValidator(1050, 1050)])),
                ('description', models.CharField(max_length=300)),
                ('is_active', models.BooleanField(default=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]