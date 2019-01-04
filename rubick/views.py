from django.shortcuts import render
from django.views.generic import ListView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from .forms import *
from underlord.views import check_login

import datetime
import uuid

import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


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
        if request.method == 'GET':
            try:
                topics = Topic.objects.all()
                for i in range(0, len(topics)):
                    topic_detail = {'topic_id': topics[i].topic_id,
                                    'title': topics[i].title,
                                    'subject': str(topics[i].subject[:50]) + '...',
                                    'like': topics[i].like,
                                    'views': topics[i].views,
                                    'created_at': topics[i].created_at,
                                    'updated_at': topics[i].updated_at,
                                    'starter': topics[i].starter}
                    topic_tag = TopicTag.objects.filter(topic__title=topic_detail['title']).all()
                    tags = []
                    for j in range(0, len(topic_tag)):
                        tag = topic_tag[j].tag
                        tag_info = {
                            'tag': tag.title,
                            'color': tag.color,
                            'color_hover': tag.color_hover
                        }
                        tags.append(tag_info)
                        topic_detail['tags'] = tags
                    self.home_topics.append(topic_detail)
                # add pages
                paginator = Paginator(self.home_topics, 5)
                page = request.GET.get('page')
                try:
                    all_topics = paginator.page(page)
                except PageNotAnInteger:
                    all_topics = paginator.page(1)
                except EmptyPage:
                    all_topics = paginator.page(paginator.num_pages)
                return render(request, self.template_name, {'all_topics': all_topics,
                                                            'data': self.data})
            except:
                self.data['ERROR_CODE'] = 'CNF500'  # can not found object
                return render(request, '500.html', {self.context_object_name: self.home_topics, 'data': self.data})
        else:
            self.data['ERROR_CODE'] = 'MNA403'  # method not allowed
            return render(request, '500.html', {'data': self.data})


@check_login
def new_topic(request):
    data = {}
    redirect_to = request.POST.get('next', request.GET.get('next', ''))
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            try:
                title = form.cleaned_data['title']
                subject = form.cleaned_data['subject']
                topic_id = str(uuid.uuid3(uuid.NAMESPACE_DNS, title)).replace('-', '')
                username = request.user.username
                starter = User.objects.filter(username=username).all()[0]
                tags = ['计算机科学与技术', '会计学']
                Topic.objects.create(topic_id=topic_id,
                                     title=title,
                                     subject=subject,
                                     starter=starter,
                                     tags=tags).save()
                data['message'] = 'CU200'  # create succeed
                return render(request, 'rubick/new_topic.html', {'form': form, 'next': redirect_to, 'data': data})
            except:
                data['ERROR_CODE'] = 'CNF500'  # can not found object
                return render(request, '500.html', {'data': data})
        else:
            data['ERROR_CODE'] = 'FNV500'  # form not valid
            return render(request, '500.html', {'data': data})
    else:
        tags = Tag.objects.all()
        form = NewTopicForm()

    return render(request, 'rubick/new_topic.html', {'form': form, 'tags': tags})


@check_login
def post_topic(request):
    data = {}
    redirect_to = request.POST.get('next', request.GET.get('next', ''))
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            try:
                message = form.cleaned_data['post']
                topic_id = form.cleaned_data['topic_id']
                topic = Topic.objects.filter(topic_id=topic_id).all()[0]
                post_id = str(uuid.uuid3(uuid.NAMESPACE_DNS, message[:10])).replace('-', '')
                username = request.user.username
                created_by = User.objects.filter(username=username).all()[0]
                updated_by = User.objects.filter(username=username).all()[0]
                logging.info(topic_id)
                Post.objects.create(post_id=post_id,
                                    message=message,
                                    topic=topic,
                                    created_by=created_by,
                                    updated_by=updated_by).save()
                return render(request, 'rubick/detail_topic.html', {'form': form, 'next': redirect_to})
            except:
                data['ERROR_CODE'] = 'CNC500'  # can not create object
                return render(request, '500.html', {'data': data})
        else:
            data['VALID_MSG'] = form.errors
            data['ERROR_CODE'] = 'FNV500'  # form not valid
            return render(request, '500.html', {'data': data})
    else:

        form = PostForm()

    return render(request, 'rubick/detail_topic.html', {'form': form})


@csrf_exempt
def get_tags(request):
    if request.method == 'POST':
        title = request.POST.get('tag')
        try:
            tag = Tag.objects.filter(title=title).all()[0]
            return JsonResponse(tag.title, safe=False)
        except:
            return JsonResponse(500, safe=False)
    else:
        return JsonResponse(500, safe=False)


@check_login
def get_topic_detail(request):
    data = {}
    if request.method == 'GET':
        try:
            topic_id = request.GET.get('topic_id')
            topic = Topic.objects.filter(topic_id=topic_id).all()[0]
            views = topic.views + 1
            _topic = Topic.objects.get(topic_id=topic_id)
            _topic.views = views
            _topic.save()
            form = PostForm(initial={'topic_id': topic_id})
            return render(request, 'rubick/detail_topic.html', {'topic': topic, 'form': form})
        except:
            data['ERROR_CODE'] = 'CNF500'  # can not found object
            return render(request, '500.html', {'data': data})
    else:
        data['ERROR_CODE'] = 'MNA403'  # method not allowed
        return render(request, '500.html', {'data': data})
