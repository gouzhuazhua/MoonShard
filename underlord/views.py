from django.shortcuts import render, redirect
from .forms import RegisterForm


# Create your views here.
def hello(request):
    return render(request, '500.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/')

    else:
        form = RegisterForm()

    return render(request, 'underlord/register.html', {'form': form})
