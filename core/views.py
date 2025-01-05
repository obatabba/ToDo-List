from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import TaskAddFrom
from .models import Task


class Login(LoginView):
    template_name = 'login.html'


class Logout(LogoutView):
    next_page = 'home'
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "You have been logged out successfully.")
        return super().dispatch(request, *args, **kwargs)
    

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def home(request):
    tasks = Task.objects.all()
    form = TaskAddFrom()
    return render(request, 'home.html', {'tasks': list(tasks), 'form': form})


def create_task(request):
    if request.method == 'POST':
        form = TaskAddFrom(request.POST)
        if form.is_valid():
            task: Task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('home')
    return redirect('home')
        