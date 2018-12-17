# -*- coding: utf-8 -*-
# @Time    : 2018/12/17 15:36
# @Author  : Invoker
# @FileName: urls.py
# @Software: PyCharm

from django.urls import path, include
from .views import *

app_name = 'rubick'
urlpatterns = [
    path('home/', ToHome().to_home, name='home'),
    path('newTopic/', new_topic, name='new_topic'),
]