# Generated by Django 3.2.8 on 2021-10-28 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0008_auto_20211028_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rooms',
            name='layer_group_name',
            field=models.CharField(default='3feb2ce8-028f-42ec-ad54-5eeceddef6e3', max_length=32),
        ),
    ]
