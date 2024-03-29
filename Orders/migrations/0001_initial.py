# Generated by Django 2.2.7 on 2020-10-04 22:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Cart', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref_no', models.CharField(default='4f55g5', max_length=50, unique=True, verbose_name='reference no')),
                ('order_status', models.CharField(choices=[('ENROUTE', 'Enroute'), ('PROCESSING', 'Processing'), ('DELIVERED', 'Delivered'), ('CANCELLED', 'Cancelled')], default='PROCESSING', max_length=50, verbose_name='order status')),
                ('refund_status', models.CharField(choices=[('REQUESTED', 'Requested'), ('GRANTED', 'Granted'), ('NO_REQUEST', 'No Request')], default='REQUESTED', max_length=50, verbose_name='refund status')),
                ('payment_method', models.CharField(choices=[('PAYONW', 'pay now'), ('PAYONDELVY', 'Pay on delivery'), ('NOPAY', 'No payment')], default='NOPAY', max_length=20, verbose_name='payment method')),
                ('delivery_method', models.CharField(choices=[('PICKUP_SITE', 'Pick-up sites'), ('DOOR_2_DOOR', 'Door-to-Door delivery')], default='DOOR_2_DOOR', max_length=50, verbose_name='delivery method')),
                ('ordered_at', models.DateTimeField(auto_now_add=True, verbose_name='date added')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='date updated')),
            ],
            options={
                'verbose_name_plural': 'Orders',
                'db_table': 'Order',
                'ordering': ['-ordered_at'],
            },
        ),
        migrations.CreateModel(
            name='OrderedItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50)),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='quantity of products')),
                ('price', models.DecimalField(decimal_places=2, default='0.00', max_digits=12, verbose_name='total price')),
                ('cart_content', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Cart.Cart', verbose_name='cart_content')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='Orders.Order', verbose_name='order')),
            ],
            options={
                'verbose_name': 'order_item',
                'verbose_name_plural': 'order_items',
                'db_table': 'order_item',
            },
        ),
    ]
