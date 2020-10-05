# Generated by Django 2.2.7 on 2020-10-04 22:48

import Products.models.itemAttribute
import Products.models.product
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'product_attribute',
            },
        ),
        migrations.CreateModel(
            name='KeyFeature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature', models.CharField(blank=True, max_length=50, verbose_name='key feature')),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'key_feature',
                'verbose_name_plural': 'key_features',
                'db_table': 'product_key_feature',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='product name')),
                ('price', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='product price')),
                ('discount', models.DecimalField(blank=True, decimal_places=2, max_digits=12, verbose_name='product discount')),
                ('brand', models.CharField(max_length=50, verbose_name='product brand')),
                ('availability', models.CharField(choices=[('IN STOCK', 'in stock'), ('OUT OF STOCK', 'out of stock')], max_length=50, verbose_name='availabilty')),
                ('sku_no', models.CharField(blank=True, max_length=50, verbose_name='SKU_NO')),
                ('attachment_1', models.ImageField(upload_to=Products.models.product.product_upload_to)),
                ('attachment_2', models.ImageField(blank=True, upload_to=Products.models.product.product_upload_to)),
                ('attachment_3', models.ImageField(blank=True, upload_to=Products.models.product.product_upload_to)),
                ('attachment_4', models.ImageField(blank=True, upload_to=Products.models.product.product_upload_to)),
                ('description_text', models.TextField(max_length=200, verbose_name='product description')),
                ('description_attachment_1', models.ImageField(blank=True, upload_to=Products.models.product.upload_to)),
                ('description_attachment_2', models.ImageField(blank=True, upload_to=Products.models.product.upload_to)),
                ('ref_no', models.CharField(blank=True, default='', max_length=100, unique=True, verbose_name='reference no')),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', mptt.fields.TreeForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='products', to='Category.Category')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
                'db_table': 'product',
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='Viewed',
            fields=[
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='Products.Product', verbose_name='product')),
                ('n_views', models.IntegerField(blank=True, default=0, verbose_name='number of views')),
                ('viewed_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'viewed',
            },
        ),
        migrations.CreateModel(
            name='Variation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor_metric', models.CharField(max_length=50)),
                ('metric_verbose_name', models.CharField(blank=True, max_length=50)),
                ('attachment', models.ImageField(blank=True, upload_to=Products.models.itemAttribute.upload_to)),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='Products.Attribute')),
            ],
            options={
                'db_table': 'attribute_variation',
            },
        ),
        migrations.CreateModel(
            name='Specification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default='', max_length=100, verbose_name='specification type')),
                ('value', models.CharField(default='', max_length=100, verbose_name='specification content')),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specifications', to='Products.Product', verbose_name='product')),
            ],
            options={
                'verbose_name': 'specification',
                'verbose_name_plural': 'specifications',
                'db_table': 'product_specification',
            },
        ),
    ]
