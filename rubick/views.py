from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from underlord.models import News
from .forms import *
from underlord.views import check_login
from notifications.signals import notify

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
        if request.method == 'GET' or request.method == 'POST':
            try:
                topics = Topic.objects.all()
                for i in range(0, len(topics)):
                    posts = Post.objects.filter(topic=topics[i]).all()
                    score_t = 2*len(Topic.objects.filter(starter=topics[i].starter).all())
                    score_p = len(Post.objects.filter(created_by=topics[i].starter).all())
                    score = score_t + score_p
                    topic_detail = {'topic_id': topics[i].topic_id,
                                    'title': topics[i].title,
                                    'subject': str(topics[i].subject[:50]) + '...',
                                    'like': topics[i].like,
                                    'posts': len(posts),
                                    'views': topics[i].views,
                                    'created_at': topics[i].created_at,
                                    'updated_at': topics[i].updated_at,
                                    'starter': topics[i].starter,
                                    'score': score}
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

                news = News.objects.all()[:6]
                return render(request, self.template_name, {'all_topics': all_topics,
                                                            'topic_amount': len(topics),
                                                            'news_6':news,
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
                tags = ['']
                Topic.objects.create(topic_id=topic_id,
                                     title=title,
                                     subject=subject,
                                     starter=request.user,
                                     tags=tags,
                                     board='rubick').save()
                data['message'] = 'CS200'  # create succeed
                return ToHome().to_home(request)
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
    # redirect_to = request.POST.get('next', request.GET.get('next', ''))
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            try:
                message = form.cleaned_data['post']
                post_id = str(uuid.uuid4()).replace('-', '')
                topic_id = form.cleaned_data['topic_id']
                topic = Topic.objects.filter(topic_id=topic_id).all()[0]
                username = request.user.username
                created_by = User.objects.filter(username=username).all()[0]
                updated_by = User.objects.filter(username=username).all()[0]
                logging.info(topic_id)
                Post.objects.create(post_id=post_id,
                                    message=message,
                                    topic=topic,
                                    created_by=created_by,
                                    updated_by=updated_by).save()
                notify.send(created_by, recipient=topic.starter, verb=topic.topic_id, level='post')
                return redirect(topic)
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
def do_reply(request):
    if request.method == 'POST':
        try:
            reply_id = str(uuid.uuid4()).replace('-', '')
            post_id = request.POST.get('post_id')
            post = Post.objects.get(post_id=post_id)
            message = request.POST.get('reply')
            user = request.user
            Reply.objects.create(reply_id=reply_id,
                                 message=message,
                                 post=post,
                                 created_by=user,
                                 updated_by=user).save()
            return JsonResponse(200, safe=False)
        except:
            return JsonResponse(500, safe=False)
    else:
        return JsonResponse(400, safe=False)


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


class ToTopicDetail(ListView):

    def __init__(self):
        super(ToTopicDetail, self).__init__()
        self.model = Post
        self.template_name = 'rubick/detail_topic.html'
        self.context_object_name = ''
        self.home_topics = []
        self.data = {}

    def get_topic_detail(self, request, topic_id):
        all_posts_db_change = []
        all_replys = []
        all_post_score = []
        data = {}
        if request.method == 'GET':
            try:
                # topic_id = request.GET.get('topic_id')
                topic = Topic.objects.filter(topic_id=topic_id).all()[0]
                views = topic.views + 1
                _topic = Topic.objects.get(topic_id=topic_id)
                _topic.views = views
                _topic.save()
                all_tags = TopicTag.objects.filter(topic=topic).all()
                all_posts_db = Post.objects.filter(topic=topic).all()
                _topics = Topic.objects.filter(starter=topic.starter).all()
                _posts = Post.objects.filter(created_by=topic.starter).all()
                topic_starter_score = 2*len(_topics) + len(_posts)
                for post in all_posts_db:
                    _p_topics = Topic.objects.filter(starter=post.created_by).all()
                    _p_posts = Post.objects.filter(created_by=post.created_by).all()
                    post_starter_score = 2 * len(_p_topics) + len(_p_posts)
                    p_score = {post.created_by: post_starter_score}
                    if p_score not in all_post_score:
                        all_post_score.append(p_score)
                    all_posts_db_change.append(post)
                    post_replys = Reply.objects.filter(post=post).all()
                    all_replys.append(post_replys)

                logging.info(all_post_score)
                form = PostForm(initial={'topic_id': topic_id})
                paginator = Paginator(all_posts_db_change, 5)
                page = request.GET.get('page')
                try:
                    all_posts = paginator.page(page)
                except PageNotAnInteger:
                    all_posts = paginator.page(1)
                except EmptyPage:
                    all_posts = paginator.page(paginator.num_pages)

                unread_msgs = request.user.notifications.unread()
                for msg in unread_msgs:

                    if msg.recipient == request.user and msg.verb == topic_id:
                        msg.mark_as_read()
                return render(request, self.template_name, {'topic': topic,
                                                            'topic_starter_score': topic_starter_score,
                                                            'all_post_score':all_post_score,
                                                            'all_tags': all_tags,
                                                            'all_posts': all_posts,
                                                            'all_replys': all_replys,
                                                            'form': form,})
            except:
                data['ERROR_CODE'] = 'CNF500'  # can not found object
                return render(request, '500.html', {'data': data})
        else:
            data['ERROR_CODE'] = 'MNA403'  # method not allowed
            return render(request, '500.html', {'data': data})


@csrf_exempt
def do_vote(request):
    if request.method == 'POST':
        try:
            user = request.user
            vote_object = request.POST.get('vote_object')
            vote_type = request.POST.get('vote_type')
            if vote_object == 'topic':
                topic_id = request.POST.get('topic_id')
                topic = Topic.objects.get(topic_id=topic_id)
                if vote_type == '0':
                    vote_0 = Vote.objects.filter(user=user,
                                                 topic=topic,
                                                 vote_type=0).all()
                    if len(vote_0) == 0:
                        topic.like += 1
                        Vote.objects.create(user=user,
                                            topic=topic,
                                            vote_type=0).save()
                    else:
                        return JsonResponse(201, safe=False)
                else:
                    vote_1 = Vote.objects.filter(user=user,
                                                 topic=topic,
                                                 vote_type=1).all()
                    if len(vote_1) == 0:
                        topic.like -= 1
                        Vote.objects.create(user=user,
                                            topic=topic,
                                            vote_type=1).save()
                    else:
                        return JsonResponse(202, safe=False)
                topic.save()
                likes = topic.like
            else:
                post_id = request.POST.get('post_id')
                post = Post.objects.get(post_id=post_id)
                if vote_type == '0':
                    vote_0 = Vote.objects.filter(user=user,
                                                 post=post,
                                                 vote_type=0).all()
                    if len(vote_0) == 0:
                        post.like += 1
                        Vote.objects.create(user=user,
                                            post=post,
                                            vote_type=0).save()
                    else:
                        return JsonResponse(201, safe=False)
                else:
                    vote_1 = Vote.objects.filter(user=user,
                                                 post=post,
                                                 vote_type=1).all()
                    if len(vote_1) == 0:
                        post.like -= 1
                        Vote.objects.create(user=user,
                                            post=post,
                                            vote_type=1).save()
                    else:
                        return JsonResponse(202, safe=False)
                post.save()
                likes = post.like

            return JsonResponse(likes, safe=False)
        except:
            return JsonResponse(500, safe=False)
    return JsonResponse(400, safe=False)


@csrf_exempt
def do_delete_post(request):
    if request.method == 'POST':
        try:
            post_id = request.POST.get('post_id')
            Post.objects.get(post_id=post_id).delete()
            return JsonResponse(200, safe=False)
        except:
            return JsonResponse(500, safe=False)
    else:
        return JsonResponse(400, safe=False)


@csrf_exempt
def do_delete_reply(request):
    if request.method == 'POST':
        try:
            reply_id = request.POST.get('reply_id')
            Reply.objects.get(reply_id=reply_id).delete()
            return JsonResponse(200, safe=False)
        except:
            return JsonResponse(500, safe=False)
    else:
        return JsonResponse(400, safe=False)
