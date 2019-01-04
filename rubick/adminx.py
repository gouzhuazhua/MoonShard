from django.contrib import admin
from .models import *
import xadmin


# Register your models here.
class TopicAdmin(object):
    list_display = ('topic_id',
                    'title',
                    'like',
                    'views',
                    'created_at',
                    'updated_at',
                    'starter',
                    'subject',)
    list_per_page = 20
    ordering = ('id',)
    list_display_links = ('title', 'subject', 'starter',)
    search_fields = ('title',)


class PostAdmin(object):
    list_display = ('post_id',
                    'message',
                    'topic',
                    'like',
                    'created_at',
                    'updated_at',
                    'created_by',
                    'updated_by',)
    list_per_page = 20
    ordering = ('id',)
    list_display_links = ('message', 'topic',)
    search_fields = ('message',)


class ReplyAdmin(object):
    list_display = ('reply_id',
                    'message',
                    'post',
                    'created_at',
                    'updated_at',
                    'created_by',
                    'updated_by',)
    list_per_page = 20
    ordering = ('id',)
    list_display_links = ('message',)
    search_fields = ('message',)


class TagAdmin(object):
    list_display = ('title',
                    'color',
                    )
    list_per_page = 20
    ordering = ('id',)
    list_display_links = ('title',)
    search_fields = ('title', 'color',)


class TopicTagAdmin(object):
    list_display = ('topic',
                    'tag',
                    )
    list_per_page = 20
    ordering = ('id',)
    list_display_links = ('topic',)
    search_fields = ('topic', 'tag',)


class LikeAdmin(object):
    list_display = ('topic',
                    'user',
                    )
    list_per_page = 20
    ordering = ('id',)
    list_display_links = ('topic',)
    search_fields = ('topic', 'user',)


class VoteAdmin(object):
    list_display = ('reply',
                    'user',
                    'vote_type',
                    )
    list_per_page = 20
    ordering = ('id',)
    list_display_links = ('reply',)
    search_fields = ('reply', 'user', 'vote_type')


xadmin.site.register(Topic, TopicAdmin)
xadmin.site.register(Post, PostAdmin)
xadmin.site.register(Reply, ReplyAdmin)
xadmin.site.register(Tag, TagAdmin)
xadmin.site.register(TopicTag, TopicTagAdmin)
xadmin.site.register(Like, LikeAdmin)
xadmin.site.register(Vote, VoteAdmin)
