# Generated by Django 3.2.10 on 2021-12-27 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0005_alter_notification_receiver'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='detail',
            field=models.CharField(max_length=225, null=True),
        ),
    ]
