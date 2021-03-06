# Generated by Django 3.2.8 on 2021-10-27 12:50

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20211027_0210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='user_background_image',
            field=models.ImageField(blank=True, null=True, upload_to=accounts.models.image_directory_path),
        ),
        migrations.AlterField(
            model_name='users',
            name='user_icon_image',
            field=models.ImageField(blank=True, null=True, upload_to=accounts.models.image_directory_path),
        ),
    ]
