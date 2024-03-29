# Generated by Django 2.2.7 on 2020-10-04 22:48

import Users.userManager
from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=100, verbose_name='address')),
                ('city', models.CharField(max_length=50, verbose_name='city')),
                ('country', models.CharField(max_length=50, verbose_name='country')),
                ('zip_code', models.CharField(blank=True, max_length=50, verbose_name='zip code')),
                ('state', models.CharField(max_length=50, verbose_name='state')),
                ('added_at', models.DateField(auto_now=True)),
            ],
            options={
                'db_table': 'address',
            },
        ),
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(max_length=50, verbose_name='first name')),
                ('middle_name', models.CharField(blank=True, default='', max_length=50, verbose_name='middle name')),
                ('last_name', models.CharField(max_length=50, verbose_name='last name')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True, verbose_name='Phone number')),
                ('user_type', models.CharField(choices=[('SELLER', 'seller'), ('BUYER', 'buyer'), ('GUEST', 'guest'), ('ADMIN', 'admin')], default='GUEST', max_length=10, verbose_name='type of user')),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff')),
                ('is_active', models.BooleanField(default=False, verbose_name='active')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='Date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', Users.userManager.MyUserManager()),
            ],
        ),
    ]
