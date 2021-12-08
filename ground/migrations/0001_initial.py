# Generated by Django 3.2.9 on 2021-11-23 16:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import ground.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('room', '0018_rename_room_id_roommessage_room'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ground',
            fields=[
                ('ground', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('ground_content', models.CharField(max_length=400)),
                ('ground_image', models.ImageField(blank=True, null=True, upload_to=ground.models.image_directory_path_ground)),
                ('post_room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='room.rooms')),
                ('post_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'ground',
            },
        ),
    ]
