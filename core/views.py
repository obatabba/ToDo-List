from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from .forms import TaskAddFrom
from .models import Task


class Login(LoginView):
    template_name = 'login.html'


class Logout(LogoutView):
    next_page = 'home'
    

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


@login_required()
def home(request):
    tasks = Task.objects.filter(user=request.user)
    for task in tasks:
        task.check_overdue()

    form = TaskAddFrom()
    return render(request, 'home.html', {'tasks': list(tasks), 'form': form})


@login_required()
def create_task(request):
    if request.method == 'POST':
        form = TaskAddFrom(request.POST)
        if form.is_valid():
            task: Task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('home')
    return redirect('home')
        

@login_required()
def check_task(request, task_id):
    """If Task.is_completed is False set it to True, otherwise set it to False."""
    task = get_object_or_404(Task, id=task_id)
    if task.user == request.user:
        if task.is_completed:
            task.is_completed = False
            task.save()
            return redirect('home')
        else:
            task.is_completed = True
            task.save()
            return redirect('home')
    else:
        return HttpResponseForbidden()
