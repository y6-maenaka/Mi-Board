# Generated by Django 3.2.10 on 2021-12-26 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stoppo', '0018_uploadfile_is_root'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadfile',
            name='file_size',
            field=models.BigIntegerField(null=True),
        ),
    ]