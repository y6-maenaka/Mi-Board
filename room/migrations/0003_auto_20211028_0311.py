# Generated by Django 3.2.8 on 2021-10-27 18:11

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0002_auto_20211028_0309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rooms',
            name='layer_group_name',
            field=models.CharField(default=uuid.UUID('87d9ca34-7eda-4531-8be1-66a79308fa1f'), max_length=32),
        ),
        migrations.AlterField(
            model_name='rooms',
            name='room_name',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
