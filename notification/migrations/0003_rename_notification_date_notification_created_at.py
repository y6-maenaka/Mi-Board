# Generated by Django 3.2.10 on 2021-12-27 19:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0002_auto_20211227_1928'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='notification_date',
            new_name='created_at',
        ),
    ]
