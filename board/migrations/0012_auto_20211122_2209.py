# Generated by Django 3.2.9 on 2021-11-22 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0011_auto_20211122_2132'),
    ]

    operations = [
        migrations.RenameField(
            model_name='goodboard',
            old_name='baord',
            new_name='board',
        ),
        migrations.RenameField(
            model_name='storeboard',
            old_name='baord',
            new_name='board',
        ),
    ]
