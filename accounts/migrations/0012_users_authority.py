# Generated by Django 3.2.10 on 2022-01-03 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_alter_users_division'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='authority',
            field=models.CharField(default='general', max_length=20),
        ),
    ]