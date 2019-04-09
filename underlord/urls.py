from django.urls import path, include
from . import views

app_name = 'underlord'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('userInfo/<str:username>/', views.to_user_info, name='userInfo'),
    path('doFollow/', views.do_follow, name='do_follow'),
    path('doCancelFollow/', views.do_cancel_follow, name='do_cancel_follow'),
    path('updateUser/', views.update_user, name='update_user'),
    path('userTopicsSelf/', views.ToUserAllTopics().all_users_topic_self, name='user_topics_self'),
    path('userTopicsOther/', views.ToUserAllTopics().all_users_topic_other, name='user_topics_other'),
    path('userFollows/', views.ToMyFollows().to_my_follows, name='to_my_follows'),
    path('toMsgBox/', views.to_msg_box, name='to_msg_box'),
    path('doMsgSend/', views.do_msg_send, name='do_msg_send'),
    path('doMarkRead/', views.do_mark_read, name='do_mark_read'),
    path('toAllUsers/', views.ToAllUsers().to_all_users, name='to_all_users'),
    path('ToAllTags/', views.ToAllTags().to_all_tags, name='to_all_tags'),
    path('ToTagTopics/', views.ToTagTopics().to_tag_topics, name='to_tag_topics'),


    path('doDeleteTopic', views.do_delete_topic, name='do_delete_topic'),
]