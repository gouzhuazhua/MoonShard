from django.contrib import admin
from .models import *
import xadmin


# Register your models here.
class FollowsAdmin(object):
    list_display = ('id',
                    'follow_by',
                    'follow_object',
                    )
    list_per_page = 20
    ordering = ('id',)
    list_display_links = ('id',)
    search_fields = ('follow_by', 'follow_object')


class NewsAdmin(object):
    list_display = ('id',
                    'news_id',
                    'title',
                    'subject'
                    )
    list_per_page = 20
    ordering = ('id',)
    list_display_links = ('news_id',)
    search_fields = ('news_id', 'title')


xadmin.site.register(Follows, FollowsAdmin)
xadmin.site.register(News, NewsAdmin)
