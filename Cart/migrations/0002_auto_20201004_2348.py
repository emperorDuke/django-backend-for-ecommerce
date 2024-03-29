# Generated by Django 2.2.7 on 2020-10-04 22:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Cart', '0001_initial'),
        ('Products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Products.Product', verbose_name='products'),
        ),
        migrations.AddField(
            model_name='cart',
            name='variants',
            field=models.ManyToManyField(to='Products.Variation', verbose_name='variants of product'),
        ),
    ]
