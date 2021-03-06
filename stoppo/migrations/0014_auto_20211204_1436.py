# Generated by Django 3.2.9 on 2021-12-04 05:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stoppo', '0013_uploadfile_extension'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uploadfile',
            name='extension',
        ),
        migrations.AddField(
            model_name='sharefile',
            name='extension',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='sharefile',
            name='shared_file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stoppo.uploadfile'),
        ),
    ]
