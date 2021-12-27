from django.db import models
from django.utils import timezone
import uuid as uuid_lib
from accounts.models import Users

# Create your models here.


def stoppo_file_path(instance, filename):
    return 'stoppo_file/{}.{}'.format(str(uuid_lib.uuid4()), filename.split('.')[-1])


class StoppoFileStructure(models.Model):
    class Meta:
        db_table = 'stoppo_file_structure'

    directory = models.UUIDField(default=uuid_lib.uuid4,
                                primary_key=True, editable=False)

    directory_name = models.CharField(max_length = 40)

    directory_owner = models.ForeignKey(Users,on_delete=models.CASCADE)

    upward_directory = models.ForeignKey('StoppoFileStructure',on_delete=models.CASCADE,null=True)

    data_type = models.CharField(max_length = 10)

    created_at = models.DateTimeField(default=timezone.now)

    is_root = models.BooleanField(default=False)

class UploadFile(models.Model):
    class Meta:
        db_table = 'upload_file'

    upload_file_id = models.UUIDField(default=uuid_lib.uuid4,
                                primary_key=True, editable=False)

    upward_directory = models.ForeignKey(StoppoFileStructure,on_delete=models.CASCADE,null=True)

    upload_user = models.ForeignKey(Users,on_delete=models.CASCADE,null=True)

    created_at = models.DateTimeField(default=timezone.now)

    file_name = models.CharField(max_length=30)

    is_root = models.BooleanField(default=False,null=True)

    file = models.FileField(
                    upload_to=stoppo_file_path,
                    null=True,
                    )

    extension = models.CharField(max_length=10,null=True)

    file_size = models.BigIntegerField(null=True)

class ShareFile(models.Model):
    class Meta:
        db_table = 'share_file'

    send_user = models.ForeignKey(Users,on_delete=models.CASCADE,related_name='send_user')

    receive_user = models.ForeignKey(Users,on_delete=models.CASCADE,related_name='receive_user')

    shared_file = models.ForeignKey(UploadFile,on_delete=models.CASCADE)

    created_at = models.DateTimeField(default=timezone.now)
