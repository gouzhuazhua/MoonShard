# -*- coding: utf-8 -*-
# @Time    : 2018/12/17 15:36
# @Author  : Invoker
# @FileName: urls.py
# @Software: PyCharm

from django.urls import path, include
from . import views

app_name = 'rubick'
urlpatterns = [
    path('home/', views.ToHome().to_home, name='home'),
    path('newTopic/', views.new_topic, name='new_topic'),
    path('getTags/', views.get_tags, name='get_tags'),
    path('<str:topic_id>/detailTopic/', views.ToTopicDetail().get_topic_detail, name='get_topic_detail'),
    path('postTopic/', views.post_topic, name='post_topic'),
    path('doReply/', views.do_reply, name='do_reply'),
    path('doVote/', views.do_vote, name='do_vote'),
    path('doDeletePost', views.do_delete_post, name='do_delete_post'),
    path('doDeleteReply', views.do_delete_reply, name='do_delete_reply'),
]
