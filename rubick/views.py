from django.shortcuts import render
from django.views.generic import ListView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import *
from .forms import *
from underlord.views import check_login

import datetime

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


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
        self.home_topics = []
        self.data.clear()
        try:
            self.home_topics = Topic.objects.all()[:20]
            return render(request, self.template_name, {self.context_object_name: self.home_topics, 'data': self.data})
        except:
            self.data['message'] = '不能获取主题。'
            return render(request, '500.html', {self.context_object_name: self.home_topics, 'data': self.data})


@check_login
def new_topic(request):
    data = {}
    redirect_to = request.POST.get('next', request.GET.get('next', ''))
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            subject = form.cleaned_data['subject']
            username = request.user.username
            starter = User.objects.filter(username=username).all()[0]
            Topic.objects.create(title=title,
                                 subject=subject,
                                 starter=starter).save()
            data['message'] = '新建主题成功。'
            return render(request, 'rubick/new_topic.html', {'form': form, 'next': redirect_to, 'data': data})
        else:
            data['message'] = form.errors
            return render(request, '500.html', {'data': data})
    else:
        tags = Tag.objects.all()
        form = NewTopicForm()

    return render(request, 'rubick/new_topic.html', {'form': form, 'tags': tags})


@csrf_exempt
def get_tags(request):
    if request.method == 'POST':
        title = request.POST.get('tag')
        logging.info('>>>>>>>>>>>>>>>' + str(title))
        try:
            tag = Tag.objects.filter(title=title).all()[0]
            logging.info('+++++++++++++++' + str(tag.title))
            return JsonResponse(tag, safe=False)
        except:
            return JsonResponse(500, safe=False)
    else:
        return JsonResponse(500, safe=False)


@check_login
def get_topic_detail(request):
    data = {}
    if request.method == 'GET':
        topic_id = request.GET.get('id')
        topic_name = request.GET.get('name')
        # topic = Topic.objects.filter(id=topic_id).all()[0]
        logging.info('>>>>>>>>>>>>>>>>>>>>> ' + str(topic_id) + ' + ' + str(topic_name))




