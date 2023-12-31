# Generated by Django 2.0.1 on 2020-07-26 12:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import products.models
import stdimage.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0052_auto_20200223_1757'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product_Refund',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField()),
                ('accepted', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Subscribers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.RenameField(
            model_name='product_description',
            old_name='categary',
            new_name='category',
        ),
        migrations.RenameField(
            model_name='product_description',
            old_name='sub_categary',
            new_name='sub_category',
        ),
        migrations.RenameField(
            model_name='product_description',
            old_name='sub_sub_categary',
            new_name='sub_sub_category',
        ),
        migrations.AddField(
            model_name='product_description',
            name='Current_City',
            field=models.CharField(default='Tokyo', max_length=30),
        ),
        migrations.AddField(
            model_name='product_description',
            name='rating',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=3),
        ),
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
            model_name='product_description',
            name='image',
            field=models.ImageField(upload_to=products.models.upload_image_path, validators=[stdimage.validators.MaxSizeValidator(1050, 1050)]),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(upload_to=products.models.upload_image_path, validators=[stdimage.validators.MaxSizeValidator(1050, 1050)]),
        ),
        migrations.AlterField(
            model_name='user_review',
            name='rating',
            field=models.IntegerField(default=5),
        ),
        migrations.AlterField(
            model_name='variation',
            name='category',
            field=models.CharField(choices=[('size', 'size'), ('color', 'color')], default='size', max_length=120),
        ),
        migrations.AddField(
            model_name='product_refund',
            name='product_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product_description'),
        ),
    ]
