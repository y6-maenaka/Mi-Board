# Generated by Django 3.2.8 on 2021-10-28 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0009_alter_rooms_layer_group_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rooms',
            name='layer_group_name',
            field=models.CharField(default='25e9b410-f6b2-4b2e-b919-c3d05d62a271', max_length=33),
        ),
    ]
