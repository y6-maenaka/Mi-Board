from django.db import models
from django.utils import timezone
from accounts.models import Users
from room.models import Rooms

# Create your models here.


class Notification(models.Model):
    class Meta:
        db_table = 'notification'

    created_at = models.DateTimeField(default=timezone.now)
    detail = models.CharField(max_length=225,null=True)
    verified = models.BooleanField(default=False)
    type = models.CharField(max_length=20)
    room = models.ForeignKey(Rooms,on_delete=models.CASCADE,null=True)
    partner = models.ForeignKey(Users,on_delete=models.CASCADE,related_name='partner_id',null=True)
    receiver = models.ForeignKey(Users,on_delete=models.CASCADE,related_name='receiver_id',null=True)
    display_name = models.CharField(max_length=20,null=True)
