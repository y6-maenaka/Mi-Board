# Generated by Django 3.2.9 on 2021-11-21 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0008_boardcomment_best_board'),
    ]

    operations = [
        migrations.AddField(
            model_name='boards',
            name='best_board',
            field=models.BooleanField(default=False),
        ),
    ]
