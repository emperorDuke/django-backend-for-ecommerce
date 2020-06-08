# Generated by Django 2.2.7 on 2020-05-04 19:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('BuyerProfile', '0001_initial'),
        ('Users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingdetail',
            name='address',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Users.Address'),
        ),
        migrations.AddField(
            model_name='shippingdetail',
            name='buyer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shipping_details', to='BuyerProfile.BuyerProfile'),
        ),
        migrations.AddField(
            model_name='buyerprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='buyer'),
        ),
    ]
