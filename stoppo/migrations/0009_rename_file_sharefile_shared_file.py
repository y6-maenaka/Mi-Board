# Generated by Django 3.2.9 on 2021-12-01 12:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stoppo', '0008_remove_sharefile_file_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sharefile',
            old_name='file',
            new_name='shared_file',
        ),
    ]
