from django.shortcuts import render
from django.views.generic import ListView
from .models import *
from .forms import *
from underlord.views import check_login

import datetime


# Create your views here.
class ToHome(ListView):

    def __init__(self):
        super(ToHome, self).__init__()
        self.model = Topic
        self.template_name = 'rubick/home.html'
        self.context_object_name = 'all_topics'
        self.home_topics = []
        self.data = {}

    def to_home(self, request):
        self.home_topics.clear()
        try:
            self.home_topics = Topic.objects.all().order_by('-created_at')[:20]
        except:
            self.data['message'] = '不能获取主题。'
            return render(request, '500.html', {self.context_object_name: self.home_topics, 'data': self.data})


@check_login
def new_topic(request):
    data = {}
    redirect_to = request.POST.get('next', request.GET.get('next', ''))
    if request.method == 'POST':
        form = NewTopicForm()
        if form.is_valid():
            title = form.cleaned_data['title']
            subject = form.cleaned_data['subject']
            now = datetime.datetime.now()
            starter = request.user.username
            Topic.objects.create(title=title,
                                 subject=subject,
                                 updated_at=now,
                                 starter=starter).save()
            data['message'] = '新建主题成功。'
            return render(request, 'rubick/new_topic.html', {'form': form, 'next': redirect_to, 'data':data})
        else:
            data['message'] = '表单验证失败'
            return render(request, '500.html', {'data': data})
    else:
        form = NewTopicForm()

    return render(request, 'rubick/new_topic.html', {'form': form})






