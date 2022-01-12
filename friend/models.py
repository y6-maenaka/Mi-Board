from django.db import models
from accounts.models import Users
from django.utils import timezone

# Create your models here.

class ViewFriendProfile(models.Model):
    class Meta:
        db_table = 'view_friend_profile'

    owner_user = models.ForeignKey(Users,on_delete=models.CASCADE,related_name='owner_user_id')
    visitor_user = models.ForeignKey(Users,on_delete=models.CASCADE,name='visitor_user')
    created_at = models.DateTimeField(default = timezone.now)
