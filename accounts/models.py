from django.db import models
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone
import uuid as uuid_lib

# Create your models here.

def image_directory_path(instance, filename):
    return 'user_image/{}.{}'.format(str(uuid_lib.uuid4()), filename.split('.')[-1])

class UserManager(UserManager):
    """ユーザーマネージャー"""
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('The given email must be set')
        username = self.normalize_email(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(username, password, **extra_fields)


class Users(AbstractBaseUser, PermissionsMixin):
    """カスタムユーザーモデル."""
    class Meta:
        db_table = 'users'
        verbose_name = ('users')
        verbose_name_plural = ('users')

    user_id = models.UUIDField(default=uuid_lib.uuid4,
                                primary_key=True, editable=False)

    username = models.CharField(
        max_length = 20,
        unique = True,
        help_text = ('Required. 20 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages = {
            'unique':('A user with that username already exists.'),
        }
    )

    email = models.EmailField(
        max_length = 254,
        blank = True,
        null = True,
    )

    #ユーザ状態の判断(ログイン状態) BAN用
    is_active = models.BooleanField(
        default = True,
    )

    #権限の判断(凍結など)
    is_staff = models.BooleanField(
        default = False,
    )

    #登録日
    created_at = models.DateTimeField(
        default = timezone.now,
    )

    #更新日
    updated_at = models.DateTimeField(
        default = timezone.now,
    )

    #ポイント
    points = models.IntegerField(
        default = 10,
        blank = False,
    )

    #大学名
    university = models.CharField(
        max_length = 10,
    )

    #苗字
    last_name = models.CharField(
        max_length = 8,
    )

    #名前
    first_name = models.CharField(
        max_length = 8,
    )

    #学部
    department = models.CharField(
        max_length = 10,
    )

    #学科
    division = models.CharField(
        max_length = 12,
    )

    #研究室
    laboratory = models.CharField(
        max_length = 10,
        blank = True,
        null = True,
    )

    #バイト先
    part_time_job = models.CharField(
        max_length = 8,
        blank = True,
        null = True,
    )

    #サークル
    circle = models.CharField(
        max_length = 8,
        blank = True,
        null = True,
    )

    #出身地
    hometown = models.CharField(
        max_length = 10,
        blank = True,
        null = True,
    )

    #出身高校
    high_school = models.CharField(
        max_length = 10,
        blank = True,
        null = True,
    )

    #詳しく
    detail = models.CharField(
        max_length = 250,
        blank = True,
        null = True,
    )

    sns_link_twitter = models.CharField(
        max_length = 254,
        blank = True,
        null = True,
    )

    sns_link_instagram = models.CharField(
        max_length = 254,
        blank = True,
        null = True,
    )

    sns_link_facebook = models.CharField(
        max_length = 254,
        blank = True,
        null = True,
    )

    #ユーザー画像
    user_icon_image = models.ImageField(
        upload_to=image_directory_path,
        blank=True,
        null=True,
    )

    #ユーザーバックグラウンド画像
    user_background_image = models.ImageField(
        upload_to=image_directory_path,
        blank=True,
        null=True,
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []


    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in
        between."""
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    # @property
    # def username(self):
    #     """username属性のゲッター
    #
    #     他アプリケーションが、username属性にアクセスした場合に備えて定義
    #     メールアドレスを返す
    #     """
    #     return self.email



class Follows(models.Model):
    class Meta:
        db_table = 'follows'

    follows_id = models.BigAutoField(primary_key = True)

    follower = models.ForeignKey(Users,on_delete=models.CASCADE,related_name='follower_id')

    follower_confirm = models.BooleanField(default=False)

    followee = models.ForeignKey(Users,on_delete=models.CASCADE,related_name='followee_id')

    followee_confirm = models.BooleanField(default=False)

    created_at = models.DateTimeField(default = timezone.now)


class PersonalChatLayerGroup(models.Model):
    class Meta:
        db_table = 'personal_chat_layer_group'

    group_name = models.UUIDField(default=uuid_lib.uuid4,
                                    primary_key = True,
                                    editable = False)

    owner_user = models.ForeignKey(Users,on_delete=models.CASCADE,related_name='owner')
    invited_user = models.ForeignKey(Users,on_delete=models.CASCADE,related_name='inviter')
    owner_bloking = models.BooleanField(default=False)
    inviter_bloking = models.BooleanField(default=False)
    last_update = models.DateTimeField(default=timezone.now)
