from django.db import models
import  uuid as uuid_lib
from django.utils import timezone
from accounts.models import Users
from room.models import Rooms

# Create your models here.

def image_directory_path_ground(instance, filename):
    return 'ground_image/{}.{}'.format(str(uuid_lib.uuid4()), filename.split('.')[-1])


class Ground(models.Model):
    class Meta:
        db_table = 'ground'

    ground_id = models.UUIDField(default=uuid_lib.uuid4,
                                primary_key=True, editable=False)

    post_user = models.ForeignKey(Users,on_delete=models.CASCADE)

    post_room = models.ForeignKey(Rooms,on_delete=models.CASCADE,null=True)

    created_at = models.DateTimeField(default=timezone.now,null=False)

    ground_content = models.CharField(max_length = 400)

    ground_image = models.ImageField(
                        upload_to = image_directory_path_ground,
                        blank = True,
                        null = True,
                        )

    ground_address = models.CharField(max_length = 20,null=True)
