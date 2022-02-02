from django.db import models
from django.utils import timezone
from accounts.models import Users
import uuid as uuid_lib
from room.models import Rooms

# Create your models here.

def board_image_path(instance, filename):
    return 'board_image/{}.{}'.format(str(uuid_lib.uuid4()), filename.split('.')[-1])

def board_file_path(instance, filename):
    return 'board_file/{}.{}'.format(str(uuid_lib.uuid4()), filename.split('.')[-1])

def board_comment_file_path(instance, filename):
    return 'board_comment_file/{}.{}'.format(str(uuid_lib.uuid4()), filename.split('.')[-1])


class Boards(models.Model):
    class Meta:
        db_table = 'boards'

    board_id = models.UUIDField(default = uuid_lib.uuid4,
                                primary_key=True,
                                editable=False)

    category = models.CharField(max_length=20,
                                    null=False
                                    )

    title = models.CharField(max_length=120,
                                    null=False)

    content = models.CharField(max_length=3000,
                                null=True)

    attached_image = models.ImageField(
        upload_to = board_image_path,
        blank = True,
        null = True,
    )

    related_department = models.CharField(
        max_length=30,
        null = True,
    )

    related_room = models.ForeignKey(Rooms,on_delete=models.CASCADE,null=True)

    attached_file = models.FileField(
        upload_to = board_file_path,
        verbose_name='添付ファイル',
        blank = True,
        null = True,
    )

    tags = models.CharField(
            max_length = 250,
            null = True,
    )

    created_at = models.DateTimeField(
            default = timezone.now
    )

    bet_points = models.IntegerField(
        null = True,
    )

    display_name = models.CharField(max_length=36,
                                    null=True)

    best_board = models.BooleanField(default=False)

    posted_by = models.ForeignKey(Users,on_delete=models.CASCADE,
                                    null=False,)

    university = models.CharField(max_length=30,null=True)


class BoardComment(models.Model):
    class Meta:
        db_table = 'board_comment'

    comment_id = models.UUIDField(default=uuid_lib.uuid4,
                                primary_key=True, editable=False)

    comment_board = models.ForeignKey(Boards,on_delete=models.CASCADE)
    comment = models.CharField(max_length=520)
    comment_image = models.ImageField(
                        upload_to = board_comment_file_path,
                        blank = True,
                        null = True,
                        )
    comment_file = models.FileField(
                        upload_to= board_comment_file_path,
                        verbose_name='添付ファイル',
                        blank = True,
                        null = True,
                        )
    comment_user = models.ForeignKey(Users,on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(
                    default = timezone.now
                    )

    display_name = models.CharField(max_length=36,
                                    null=True)

    comment_nickname = models.CharField(max_length=36,null=True)

    best_board = models.BooleanField(default=False)

class PurchaseHistory(models.Model):
    class Meta:
        db_table = 'purchase_history'

    purchase_user = models.ForeignKey(Users,on_delete=models.CASCADE)
    purchase_board = models.ForeignKey(Boards,on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)


class GoodBoard(models.Model):
    class Meta:
        db_table = 'good_board'

    board = models.ForeignKey(Boards,on_delete=models.CASCADE)
    good_user = models.ForeignKey(Users,on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

class StoreBoard(models.Model):
    class Meta:
        db_table = 'store_board'

    board = models.ForeignKey(Boards,on_delete=models.CASCADE)
    store_user = models.ForeignKey(Users,on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
