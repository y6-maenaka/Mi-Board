from django.db import models
from room.models import Rooms
from accounts.models import Users
from django.utils import timezone
# Create your models here.

class TimeTable(models.Model):
    class Meta:
        db_table = 'timetable'

    room = models.ForeignKey(Rooms,on_delete=models.CASCADE)
    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    spot = models.CharField(null=False,max_length=5)
    created_at = models.DateTimeField(default=timezone.now)
