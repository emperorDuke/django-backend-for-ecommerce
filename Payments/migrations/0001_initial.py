# Generated by Django 2.2.7 on 2020-05-04 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=15, unique=True)),
                ('amount', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref_no', models.CharField(default='dfr44f', max_length=50, unique=True, verbose_name='reference number')),
                ('amount', models.FloatField()),
                ('status', models.CharField(choices=[('paid', 'PAID'), ('not paid', 'NOT_PAID')], default='not paid', max_length=50, verbose_name='payment status')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
