from django.db import models
from accounts.models import Users
from django.utils import timezone

# Create your models here.


class Report(models.Model):
    class Meta:
        db_table = 'report'

    user = models.ForeignKey(Users,on_delete = models.CASCADE)
    report = models.CharField(max_length=500)
    created_at = models.DateTimeField(default=timezone.now)
