# Generated by Django 3.2.9 on 2021-12-01 12:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stoppo', '0007_rename_file_id_sharefile_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sharefile',
            name='file_name',
        ),
    ]
