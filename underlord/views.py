from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt

from django.db.models.signals import post_save
from notifications.signals import notify

from rubick.models import Topic as rubick_topic, Post as rubick_post, TopicTag as rubick_topic_tag, Tag as rubick_tag
from .forms import RegisterForm, UpdateForm
from .models import *


import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


# Create your views here.
def check_login(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = AuthenticationForm()
            data = {'message': '您还未登录，请先登录'}
            return render(request, 'registration/login.html', {'form': form, 'data': data})
        else:
            return func(request, *args, **kwargs)
    return wrapper


def index(request):
    return render(request, 'index.html')


def register(request):
    redirect_to = request.POST.get('next', request.GET.get('next', ''))
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'underlord/register.html', {'form': form, 'next': redirect_to})


@check_login
def to_user_info(request, username):
    user = User.objects.get(username=username)
    request_user = request.user
    user_topic = rubick_topic.objects.filter(starter=user).all()
    user_post = rubick_post.objects.filter(created_by=user).all()
    all_topics = []
    topic_tags = {}

    for topic in user_topic:
        all_topics.append(topic)

    for post in user_post:
        topic = rubick_post.objects.get(post_id=post.post_id).topic
        all_topics.append(topic)

    for topic in all_topics:
        for tag in rubick_topic_tag.objects.filter(topic=topic).all():
            tag_names = []
            for key in topic_tags:
                tag_names.append(key)
            if len(topic_tags) != 0:
                for tag_name in tag_names:
                    if tag.tag == tag_name:
                        topic_tags[tag.tag] += 1
                        break
                    else:
                        topic_tags[tag.tag] = 1
            else:
                topic_tags[tag.tag] = 1

    follow_record = Follows.objects.filter(follow_object=user, follow_by=request_user).all()
    follow_record_len = len(follow_record)
    return render(request, 'underlord/user_info.html', {'user': user,
                                                        'follow_record_len': follow_record_len,
                                                        'user_tags': topic_tags,
                                                        'now_user': user})


@csrf_exempt
def do_follow(request):
    if request.method == 'POST':
        try:
            follow_object_username = request.POST.get('follow_object_username')
            follow_by = request.user
            follow_object = User.objects.get(username=follow_object_username)
            Follows.objects.create(follow_by=follow_by,
                                   follow_object=follow_object).save()
            return JsonResponse(200, safe=False)
        except:
            return JsonResponse(500, safe=False)
    else:
        return JsonResponse(400, safe=False)


@csrf_exempt
def do_cancel_follow(request):
    if request.method == 'POST':
        try:
            follow_object_username = request.POST.get('follow_object_username')
            follow_by = request.user
            follow_object = User.objects.get(username=follow_object_username)
            Follows.objects.get(follow_by=follow_by,
                                follow_object=follow_object).delete()
            return JsonResponse(200, safe=False)
        except:
            return JsonResponse(500, safe=False)
    else:
        return JsonResponse(400, safe=False)


@check_login
def update_user(request):
    data = {}
    redirect_to = request.POST.get('next', request.GET.get('next', ''))
    if request.method == 'POST':
        form = UpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            data['message'] = '更新个人资料成功。'
            return render(request, 'underlord/update.html', {'form': form, 'next': redirect_to, 'data': data})
        else:
            data['message'] = form.errors
    else:
        username = request.user.username
        user = User.objects.filter(username=username).all()[0]
        form = UpdateForm(initial={
            'username': user.username,
            'sex': user.sex,
            'age': user.age,
            'introduce': user.introduce,
            'addr': user.addr,
        })

    return render(request, 'underlord/update.html', {'form': form, 'next': redirect_to, 'data': data})


class ToUserAllTopics(ListView):
    def __init__(self):
        super(ToUserAllTopics, self).__init__()
        self.model_t = rubick_topic
        self.model_p = rubick_post

    def all_users_topic_self(self, request):
        if request.method == 'GET':
            try:
                user_topics_self = self.model_t.objects.filter(starter=request.user).all()
                paginator_self = Paginator(user_topics_self, 5)
                page = request.GET.get('page')
                try:
                    user_topics_self_page = paginator_self.page(page)
                except PageNotAnInteger:
                    user_topics_self_page = paginator_self.page(1)
                except EmptyPage:
                    user_topics_self_page = paginator_self.page(paginator_self.num_pages)

                return render(request, 'underlord/user_topics.html', {'topics_self': user_topics_self_page,})
            except:
                return render(request, '500.html')

    def all_users_topic_other(self, request):
        if request.method == 'GET':
            # try:
            user_topics_other = []
            posts = self.model_p.objects.filter(created_by=request.user).all()
            for post in posts:
                if post.topic not in user_topics_other:
                    user_topics_other.append(post.topic)
            logging.info(user_topics_other)

            paginator_other = Paginator(user_topics_other, 5)
            page = request.GET.get('page')
            try:
                user_topics_other_page = paginator_other.page(page)
            except PageNotAnInteger:
                user_topics_other_page = paginator_other.page(1)
            except EmptyPage:
                user_topics_other_page = paginator_other.page(paginator_other.num_pages)

            return render(request, 'underlord/user_topics_other.html', {'topics_other': user_topics_other_page, })
            # except:
            #     return render(request, '500.html')


@csrf_exempt
def do_delete_topic(request):
    if request.method == 'POST':
        try:
            topic_id = request.POST.get('topic_id')
            board = request.POST.get('board')
            if board == 'rubick':
                rubick_topic.objects.get(topic_id=topic_id).delete()
            return JsonResponse(200, safe=False)
        except:
            return JsonResponse(500, safe=False)
    else:
        return JsonResponse(400, safe=False)


class ToMyFollows(ListView):
    def __init__(self):
        super(ToMyFollows, self).__init__()
        self.model = Follows

    def to_my_follows(self, request):
        if request.method == 'GET':
            try:
                user = request.user
                user_follows_db = self.model.objects.filter(follow_by=user).all()
                user_follows = Paginator(user_follows_db, 5)
                page = request.GET.get('page')
                try:
                    user_follows_page = user_follows.page(page)
                except PageNotAnInteger:
                    user_follows_page = user_follows.page(1)
                except EmptyPage:
                    user_follows_page = user_follows.page(user_follows.num_pages)
                return render(request, 'underlord/user_follows.html', {'user_follows': user_follows_page})
            except:
                return render(request, '500.html')
        else:
            return render(request, '500.html')


def to_msg_box(request):
    if request.method == 'GET':
        # try:
        msg_object_name = request.GET.get('username')
        msg_object = User.objects.get(username=msg_object_name)
        msg_content = []
        msg_content_update = []
        msg_content_unread_to = msg_object.notifications.unread()
        msg_content_read_to = msg_object.notifications.read()
        for msg_1 in msg_content_read_to:
            if msg_1.actor == request.user and msg_1.level == 'info':
                msg_content.append(msg_1)
        for msg_2 in msg_content_unread_to:
            if msg_2.actor == request.user and msg_2.level == 'info':
                msg_content.append(msg_2)
        # msg_object.notifications.mark_all_as_read()
        msg_content_unread_from = request.user.notifications.unread()
        msg_content_read_from = request.user.notifications.read()
        for msg_1 in msg_content_read_from:
            if msg_1.actor == msg_object and msg_1.level == 'info':
                msg_content.append(msg_1)
        for msg_2 in msg_content_unread_from:
            if msg_2.actor == msg_object and msg_2.level == 'info':
                msg_content.append(msg_2)

        for i in range(0, len(msg_content)):
            for j in range(i+1, len(msg_content)):
                if msg_content[i].timestamp > msg_content[j].timestamp:
                    msg_content[i], msg_content[j] = msg_content[j], msg_content[i]

        logging.info(msg_content)
        return render(request, 'underlord/send_msg.html', {'msg_object': msg_object,
                                                           'msg_content': msg_content})
        # except:
        #     return render(request, '500.html')
    else:
        return render(request, '500.html')


@csrf_exempt
def do_msg_send(request):
    if request.method == 'POST':
        try:
            user_from = request.user
            user_to_name = request.POST.get('msg_object_name')
            user_to = User.objects.get(username=user_to_name)
            msg_content = request.POST.get('msg_content')

            notify.send(user_from, recipient=user_to, verb=msg_content)
            return JsonResponse(200, safe=False)
        except:
            return JsonResponse(500, safe=False)
    else:
        return JsonResponse(400, safe=False)


@csrf_exempt
def do_mark_read(request):
    if request.method == 'POST':
        try:
            user_from = request.user
            user_to_name = request.POST.get('msg_object_name')
            user_to = User.objects.get(username=user_to_name)

            unread_msgs = user_from.notifications.unread()
            for msg in unread_msgs:
                if msg.actor == user_to and msg.level == 'info':
                    msg.mark_as_read()
            return JsonResponse(200, safe=False)
        except:
            return JsonResponse(500, safe=False)
    else:
        return JsonResponse(400, safe=False)


class ToAllUsers(ListView):
    def __init__(self):
        super(ToAllUsers, self).__init__()
        self.model = User

    def to_all_users(self, request):
        users = []

        all_users_db = self.model.objects.all()

        for _user in all_users_db:
            user = {}
            _topics = rubick_topic.objects.filter(starter=_user).all()
            _posts = rubick_post.objects.filter(created_by=_user).all()
            user_tags = []
            for _topic in _topics:
                topic_tags = rubick_topic_tag.objects.filter(topic=_topic).all()
                for topic_tag in topic_tags:
                    if topic_tag.tag not in user_tags:
                        user_tags.append(topic_tag.tag)
            user['info'] = _user
            user['tags'] = user_tags
            user['score'] = len(_posts) + 2*len(_topics)
            users.append(user)
        logging.info(users)
        paginator_users = Paginator(users, 10)
        page = request.GET.get('page')
        try:
            paginator_users_page = paginator_users.page(page)
        except PageNotAnInteger:
            paginator_users_page = paginator_users.page(1)
        except EmptyPage:
            paginator_users_page = paginator_users.page(paginator_users.num_pages)

        return render(request, 'underlord/all_users.html', {'paginator_users_page': paginator_users_page})


class ToAllTags(ListView):
    def __init__(self):
        super(ToAllTags, self).__init__()
        self.model_rt = rubick_tag
        self.model_rtt = rubick_topic_tag

    def to_all_tags(self, request):
        tags = []
        rubick_tags = self.model_rt.objects.all()
        rubick_topic_tags = self.model_rtt.objects.all()
        for rubick_tag in rubick_tags:
            tag = {}
            tag['tag'] = rubick_tag
            tag['count'] = 0
            for rt in rubick_topic_tags:
                if rubick_tag == rt.tag:
                    tag['count'] += 1
            tags.append(tag)
        paginator_tags = Paginator(tags, 16)
        page = request.GET.get('page')
        try:
            paginator_tags_page = paginator_tags.page(page)
        except PageNotAnInteger:
            paginator_tags_page = paginator_tags.page(1)
        except EmptyPage:
            paginator_tags_page = paginator_tags.page(paginator_tags.num_pages)

        return render(request, 'underlord/all_tags.html', {'paginator_tags_page': paginator_tags_page})


class ToTagTopics(ListView):
    def __init__(self):
        super(ToTagTopics, self).__init__()
        self.model_rubick_topic = rubick_topic
        self.model_rt = rubick_tag
        self.model_rubick_topic_tag = rubick_topic_tag
        self.topics = []

    def to_tag_topics(self, request):
        self.topics.clear()
        tag_board = request.GET.get('tag_board')
        tag_name = request.GET.get('tag_name')
        if tag_board == 'rubick':
            topic_tags = self.model_rubick_topic_tag.objects.all()
            for _tt in topic_tags:
                if _tt.tag.title == tag_name:
                    logging.info(_tt.tag.title + '>>>' + tag_name)
                    self.topics.append(_tt.topic)

        paginator_topics = Paginator(self.topics, 5)
        page = request.GET.get('page')
        try:
            paginator_topics_page = paginator_topics.page(page)
        except PageNotAnInteger:
            paginator_topics_page = paginator_topics.page(1)
        except EmptyPage:
            paginator_topics_page = paginator_topics.page(paginator_topics.num_pages)

        return render(request, 'underlord/tag_topics.html', {'paginator_topics_page': paginator_topics_page,
                                                             'tag_name': tag_name,
                                                             'topics_count': len(self.topics)})
