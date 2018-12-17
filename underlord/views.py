from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import RegisterForm, UpdateForm
from .models import *


import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


# Create your views here.
def hello(request):
    return render(request, '500.html')


def check_login(func):
    def wrapper(request):
        if not request.user.is_authenticated:
            form = AuthenticationForm()
            data = {'message': '您还未登录，请先登录'}
            return render(request, 'registration/login.html', {'form': form, 'data': data})
        else:
            return func(request)

    return wrapper


def index(request):
    return render(request, 'index.html')


def register(request):
    redirect_to = request.POST.get('next', request.GET.get('next', ''))

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = RegisterForm()

    return render(request, 'underlord/register.html', {'form': form, 'next': redirect_to})


@check_login
def update_user(request):
    data = {}
    redirect_to = request.POST.get('next', request.GET.get('next', ''))
    if request.method == 'POST':
        form = UpdateForm(request.POST)
        if form.is_valid():
            sex = form.cleaned_data['sex']
            age = form.cleaned_data['age']
            request.user.sex = sex
            request.user.age = age
            request.user.save()
            data['message'] = '更新个人资料成功。'
            return render(request, 'underlord/update.html', {'form': form, 'next': redirect_to, 'data': data})
        else:
            data['message'] = '表单验证失败。'
    else:
        username = request.user.username
        user = User.objects.filter(username=username).all()[0]
        form = UpdateForm(initial={
            'sex': user.sex,
            'age': user.age,
        })

    return render(request, 'underlord/update.html', {'form': form, 'next': redirect_to, 'data': data})
