# Generated by Django 2.2.7 on 2020-10-04 22:48

import AdminAdvert.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminAdvert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='name of image')),
                ('attachment', models.ImageField(null=True, upload_to=AdminAdvert.models.upload_to)),
                ('position', models.CharField(choices=[('MAIN', 'main block'), ('CENTER', 'center block'), ('SIDE', 'side block')], max_length=30, verbose_name='position of images')),
                ('added_at', models.DateField(auto_now=True)),
            ],
            options={
                'verbose_name': 'admin_ad',
                'verbose_name_plural': 'admin_ads',
                'db_table': 'admin_ad',
                'ordering': ['-added_at'],
                'unique_together': {('name', 'attachment')},
            },
        ),
    ]
