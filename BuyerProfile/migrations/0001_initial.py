# Generated by Django 2.2.7 on 2020-05-04 19:06

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BuyerProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='date updated')),
            ],
        ),
        migrations.CreateModel(
            name='ShippingDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, verbose_name='first name')),
                ('middle_name', models.CharField(blank=True, default='', max_length=50, verbose_name='middle name')),
                ('last_name', models.CharField(max_length=50, verbose_name='last name')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Phone number')),
                ('default', models.BooleanField(default=False)),
                ('added_at', models.DateField(auto_now=True)),
            ],
        ),
    ]
