# Generated by Django 2.2.7 on 2020-05-04 19:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Products', '0001_initial'),
        ('Payments', '0001_initial'),
        ('Orders', '0001_initial'),
        ('Location', '0001_initial'),
        ('BuyerProfile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordereditem',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Products.Product', verbose_name='products'),
        ),
        migrations.AddField(
            model_name='ordereditem',
            name='variants',
            field=models.ManyToManyField(to='Products.Variation', verbose_name='variant of product'),
        ),
        migrations.AddField(
            model_name='order',
            name='buyer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='BuyerProfile.BuyerProfile', verbose_name='buyer'),
        ),
        migrations.AddField(
            model_name='order',
            name='coupons',
            field=models.ManyToManyField(related_name='orders', to='Payments.Coupon', verbose_name='coupon'),
        ),
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order', to='Payments.Payment', verbose_name='payment'),
        ),
        migrations.AddField(
            model_name='order',
            name='pickup_site',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Location.Location'),
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_detail',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='BuyerProfile.ShippingDetail'),
        ),
    ]
