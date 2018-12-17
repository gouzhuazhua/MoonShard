from django.contrib import admin
from .models import *
import xadmin


# Register your models here.
class TopicAdmin(object):
    list_display = ('title',
                    'subject',
                    'like',
                    'views',
                    'created_at',
                    'updated_at',
                    'starter',)
    list_per_page = 20
    ordering = ('id',)
    list_display_links = ('title',)
    search_fields = ('title',)


class PostAdmin(object):
    list_display = ('message',
                    'topic',
                    'like',
                    'created_at',
                    'updated_at',
                    'created_by',
                    'updated_by',)
    list_per_page = 20
    ordering = ('id',)
    list_display_links = ('message',)
    search_fields = ('message',)


class ReplyAdmin(object):
    list_display = ('message',
                    'post',
                    'created_at',
                    'updated_at',
                    'created_by',
                    'updated_by',)
    list_per_page = 20
    ordering = ('id',)
    list_display_links = ('message',)
    search_fields = ('message',)


xadmin.site.register(Topic, TopicAdmin)
xadmin.site.register(Post, PostAdmin)
xadmin.site.register(Reply, ReplyAdmin)
