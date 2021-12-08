from django.db import models
from django.utils import timezone
import uuid as uuid_lib
from accounts.models import Users

# Create your models here.

def image_directory_path(instance, filename):
    return 'room_image/{}.{}'.format(str(uuid_lib.uuid4()), filename.split('.')[-1])


class Rooms(models.Model):
    class Meta:
        db_table = 'rooms'

    #room_idをlayer_group_nameとしても使う
    room_id = models.UUIDField(default=uuid_lib.uuid4,
                                primary_key=True, editable=False)

    room_name = models.CharField(max_length = 10,
                                unique = True,
                                null = False,
                                )

    university = models.CharField(max_length = 30)

    representative_person_name = models.CharField(max_length = 10)

    category = models.CharField(max_length=20,
                                    null=False
                                    )
    work_time = models.IntegerField(null=True)

    subject_to = models.CharField(max_length=20,
                        null=True)

    created_at = models.DateTimeField(default=timezone.now)

    week_at = models.CharField(max_length=10,null=True)

    room_image = models.ImageField(
        upload_to = image_directory_path,
        blank = True,
        null = True,
    )

class RoomJoining(models.Model):
    class Meta:
        db_table = 'room_joining'

    joininig_id = models.BigAutoField(primary_key=True)
    room = models.ForeignKey(Rooms,on_delete = models.CASCADE,related_name='joining_room_id')
    user = models.ForeignKey(Users,on_delete = models.CASCADE,related_name='joining_user_id')
    spot_id = models.IntegerField(null=True)


class RoomMessage(models.Model):
    class Meta:
        db_table = 'room_message'

    room = models.ForeignKey(Rooms,on_delete = models.CASCADE)
    message = models.CharField(max_length=250)
    created_at = models.DateTimeField(default=timezone.now)
    send_user = models.ForeignKey(Users,on_delete=models.CASCADE)
