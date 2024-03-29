# Generated by Django 2.2.7 on 2020-10-04 22:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Users', '0001_initial'),
        ('Stores', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='address',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Users.Address'),
        ),
        migrations.AddField(
            model_name='store',
            name='merchant',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='advert',
            name='store',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Stores.Store', verbose_name='store'),
        ),
    ]
