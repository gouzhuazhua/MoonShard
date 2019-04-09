from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
# Create your models here.


class User(AbstractUser):
    avatar = ProcessedImageField(upload_to='avatar/',
                                 default='avatar/default.png',
                                 blank=True,
                                 verbose_name='头像',)
    introduce = models.CharField(max_length=255, verbose_name='简介', default='')
    age = models.IntegerField(default=0, verbose_name='年龄')
    SEX_CHOICE = (
        ('0', '未确认'),
        ('1', '男'),
        ('2', '女'),
    )
    sex = models.CharField(max_length=6, choices=SEX_CHOICE, verbose_name='性别')
    addr = models.CharField(max_length=255, verbose_name='公寓地址', default='')

    class Meta(AbstractUser.Meta):
        pass


class Follows(models.Model):
    follow_by = models.ForeignKey(User, null=True, blank=True, related_name='follows_follow_by', on_delete=models.SET_NULL, verbose_name='关注者')
    follow_object = models.ForeignKey(User, null=True, blank=True, related_name='follows_follow_object', on_delete=models.SET_NULL, verbose_name='关注对象')


class News(models.Model):
    news_id = models.CharField(max_length=32, verbose_name='资讯编号', unique=True)
    title = models.CharField(max_length=100, verbose_name='资讯标题', unique=True)
    subject = models.TextField(max_length=4000, verbose_name='资讯内容')
