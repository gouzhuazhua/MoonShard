from django.db import models
from underlord.models import User


# Create your models here.
class Topic(models.Model):
    title = models.CharField(max_length=100, verbose_name='主题标题', unique=True)
    subject = models.TextField(max_length=4000, verbose_name='主题内容')
    like = models.IntegerField(default=0, verbose_name='点赞数')
    views = models.IntegerField(default=0, verbose_name='浏览数')
    created_at = models.DateTimeField(verbose_name='创建时间')
    updated_at = models.DateTimeField(verbose_name='更新时间')
    starter = models.ForeignKey(User, related_name='topics_starter', on_delete=True, verbose_name='发起者')

    def __str__(self):
        return self.title


class Post(models.Model):
    message = models.TextField(max_length=4000, verbose_name='回复内容')
    topic = models.ForeignKey(Topic, related_name='posts_topic', on_delete=True, verbose_name='关联主题')
    like = models.IntegerField(default=0, verbose_name='点赞数')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='回复时间')
    updated_at = models.DateTimeField(null=True, verbose_name='更新时间')
    created_by = models.ForeignKey(User, related_name='posts_created_by', on_delete=True, verbose_name='回复者')
    updated_by = models.ForeignKey(User, null=True, related_name='posts_updated_by', on_delete=True, verbose_name='更新者')

    def __str__(self):
        return self.message


class Reply(models.Model):
    message = models.CharField(max_length=255, verbose_name='评论回复')
    post = models.ForeignKey(Post, related_name='reply_post', on_delete=True, verbose_name='关联回复')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='回复时间')
    updated_at = models.DateTimeField(null=True, verbose_name='更新时间')
    created_by = models.ForeignKey(User, related_name='reply_created_by', on_delete=True, verbose_name='回复者')
    updated_by = models.ForeignKey(User, null=True, related_name='reply_updated_by', on_delete=True, verbose_name='更新者')

    def __str__(self):
        return self.message
