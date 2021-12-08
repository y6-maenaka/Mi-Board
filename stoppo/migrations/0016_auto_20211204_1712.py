# Generated by Django 3.2.9 on 2021-12-04 08:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stoppo', '0015_auto_20211204_1437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sharefile',
            name='receive_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='receive_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='sharefile',
            name='send_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='send_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='sharefile',
            name='shared_file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='stoppo.uploadfile'),
        ),
        migrations.AlterField(
            model_name='uploadfile',
            name='upload_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='uploadfile',
            name='upward_directory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='stoppo.stoppofilestructure'),
        ),
    ]
