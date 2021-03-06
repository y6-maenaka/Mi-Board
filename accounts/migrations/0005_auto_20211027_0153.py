# Generated by Django 3.2.8 on 2021-10-26 16:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20211027_0151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follows',
            name='followee_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followee_id', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='follows',
            name='follower_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower_id', to=settings.AUTH_USER_MODEL),
        ),
    ]
