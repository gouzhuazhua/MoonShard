from django.db import models
from django.urls import reverse

from underlord.models import User


# Create your models here.
class Topic(models.Model):
    topic_id = models.CharField(max_length=32, verbose_name='主题编号', unique=True)
    title = models.CharField(max_length=100, verbose_name='主题标题', unique=True)
    subject = models.TextField(max_length=4000, verbose_name='主题内容')
    like = models.IntegerField(default=0, verbose_name='点赞数')
    views = models.IntegerField(default=0, verbose_name='浏览数')
    tags = models.CharField(max_length=255, verbose_name='标签', null=True)
    board = models.CharField(max_length=255, verbose_name='板块', null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    starter = models.ForeignKey(User, related_name='topics_starter', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='发起者')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('rubick:get_topic_detail', kwargs={'topic_id': self.topic_id})


class Post(models.Model):
    post_id = models.CharField(max_length=32, verbose_name='回复编号', unique=True)
    message = models.TextField(max_length=4000, verbose_name='回复内容')
    topic = models.ForeignKey(Topic, related_name='posts_topic', null=True, blank=True, on_delete=models.CASCADE, verbose_name='关联主题')
    like = models.IntegerField(default=0, verbose_name='点赞数')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='回复时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间', null=True)
    created_by = models.ForeignKey(User, related_name='posts_created_by', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='回复者')
    updated_by = models.ForeignKey(User, related_name='posts_updated_by', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='更新者')

    def __str__(self):
        return self.message


class Reply(models.Model):
    reply_id = models.CharField(max_length=32, verbose_name='级联回复编号', unique=True)
    message = models.CharField(max_length=255, verbose_name='评论回复')
    post = models.ForeignKey(Post, related_name='reply_post', null=True, blank=True, on_delete=models.CASCADE, verbose_name='关联回复')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='回复时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间', null=True)
    created_by = models.ForeignKey(User, related_name='reply_created_by', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='回复者')
    updated_by = models.ForeignKey(User, related_name='reply_updated_by', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='更新者')

    def __str__(self):
        return self.message


class Like(models.Model):
    topic = models.ForeignKey(Topic, related_name='like_topic', null=True, blank=True, on_delete=models.CASCADE, verbose_name='喜欢的帖子')
    user = models.ForeignKey(User, related_name='like_user', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='收藏者')


class Vote(models.Model):
    topic = models.ForeignKey(Topic, related_name='vote_topic', null=True, blank=True, on_delete=models.CASCADE, verbose_name='投票主题')
    post = models.ForeignKey(Post, related_name='vote_post', null=True, blank=True, on_delete=models.CASCADE, verbose_name='投票回复')
    user = models.ForeignKey(User, related_name='vote_user', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='投票者')
    vote_type = models.IntegerField(default=0, verbose_name='投票类型')


class Tag(models.Model):
    title = models.CharField(max_length=20, verbose_name='标签名称', unique=True)
    introduce = models.CharField(max_length=255, verbose_name='标签描述', blank=True)
    board = models.CharField(max_length=255, verbose_name='所属板块', blank=True)
    color = models.CharField(max_length=7, verbose_name='标签颜色')
    color_hover = models.CharField(max_length=7, verbose_name='hove颜色')

    def __str__(self):
        return self.title


class TopicTag(models.Model):
    topic = models.ForeignKey(Topic, null=True, blank=True, on_delete=models.CASCADE, verbose_name='主题')
    tag = models.ForeignKey(Tag, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='标签')

