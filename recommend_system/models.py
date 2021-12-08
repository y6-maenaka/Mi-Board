from django.db import models
from accounts.models import Users
from board.models import Boards
from django.utils import timezone

# Create your models here.

class BrowsingHistory(models.Model):
    class Meta:
        db_table = 'browsing_history'

    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    board = models.ForeignKey(Boards,on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)


class SearchHistory(models.Model):
    class Meta:
        db_table = 'Search_history'

    search_user = models.ForeignKey(Users,on_delete=models.CASCADE,null=False)
    search_word = models.CharField(max_length=50)
    created_at = models.DateTimeField(default = timezone.now)
