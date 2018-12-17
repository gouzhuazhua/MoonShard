from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    age = models.IntegerField(default=0, verbose_name='年龄')
    SEX_CHOICE = (
        ('0', '未确认'),
        ('1', '男'),
        ('2', '女'),
    )
    sex = models.CharField(max_length=6, choices=SEX_CHOICE)

    class Meta(AbstractUser.Meta):
        pass
