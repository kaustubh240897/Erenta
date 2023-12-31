# Generated by Django 2.0.1 on 2019-08-03 20:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0028_review_timestamp'),
    ]

    operations = [
        migrations.CreateModel(
            name='Supplier_Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.EmailField(blank=True, default=None, max_length=254, null=True)),
                ('rating', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], default=5, max_length=10)),
                ('review', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('email', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RenameModel(
            old_name='Review',
            new_name='User_Review',
        ),
    ]
