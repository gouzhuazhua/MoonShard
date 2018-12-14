from django.shortcuts import render, redirect
from .forms import RegisterForm, UpdateForm


# Create your views here.
def hello(request):
    return render(request, '500.html')


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


def update_user(request):
    redirect_to = request.POST.get('next', request.GET.get('next', ''))
    if request.method == 'POST':
        form = UpdateForm(request.POST)
        if form.is_valid():
            
            return redirect('/')
    else:
        form = UpdateForm()

    return render(request, 'underlord/update.html', {'form': form, 'next': redirect_to})
