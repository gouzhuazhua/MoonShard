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
    path('detailTopic/', views.get_topic_detail, name='get_topic_detail'),
]
