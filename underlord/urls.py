from django.urls import path, include
from . import views

app_name = 'underlord'
urlpatterns = [
    path('underlord/hello/', views.hello, name='hi'),
    path('register/', views.register, name='register'),
    path('updateUser/', views.update_user, name='update_user'),
]