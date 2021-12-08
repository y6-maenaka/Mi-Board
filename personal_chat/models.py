from django.db import models
from accounts.models import PersonalChatLayerGroup, Users
from django.utils import timezone

# Create your models here.

class Message(models.Model):
    class Meta:
        db_table = 'message'

    group_name = models.ForeignKey(PersonalChatLayerGroup,on_delete=models.CASCADE)
    send_user = models.ForeignKey(Users,on_delete=models.CASCADE)
    send_by = models.DateTimeField(default=timezone.now)
    message = models.CharField(max_length=255,null=False,default='')
