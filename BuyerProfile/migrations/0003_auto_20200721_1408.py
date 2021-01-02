# Generated by Django 2.2.7 on 2020-07-21 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0002_auto_20200504_2006'),
        ('Stores', '0004_advert'),
        ('BuyerProfile', '0002_auto_20200504_2006'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyerprofile',
            name='items_viewed',
            field=models.ManyToManyField(blank=True, related_name='users_viewed', to='Products.Product'),
        ),
        migrations.AddField(
            model_name='buyerprofile',
            name='stores_followed',
            field=models.ManyToManyField(blank=True, related_name='users_following', to='Stores.Store'),
        ),
        migrations.AddField(
            model_name='buyerprofile',
            name='wish_list',
            field=models.ManyToManyField(blank=True, related_name='users_wishlist', to='Products.Product'),
        ),
    ]