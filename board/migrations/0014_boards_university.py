# Generated by Django 3.2.9 on 2021-12-07 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0013_boards_related_room'),
    ]

    operations = [
        migrations.AddField(
            model_name='boards',
            name='university',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
