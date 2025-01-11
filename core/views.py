from datetime import timedelta
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
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
    
    old_tasks = tasks.filter(
        deadline__lte=Task.default_deadline() - timedelta(days=2))
    
    yesterday_tasks = tasks.filter(
        deadline__gt=Task.default_deadline() - timedelta(days=2),
        deadline__lte=Task.default_deadline() - timedelta(days=1))

    today_tasks = tasks.filter(
        deadline__gt=Task.default_deadline() - timedelta(days=1),
        deadline__lte=Task.default_deadline())
    
    tomorrow_tasks = tasks.filter(
        deadline__gt=Task.default_deadline(),
        deadline__lte=Task.default_deadline() + timedelta(days=1))

    scheduled_tasks = tasks.filter(
        deadline__gt=Task.default_deadline() + timedelta(days=1))
    
    form = TaskAddFrom()
    context = {
        'old_tasks': list(old_tasks),
        'yesterday_tasks': list(yesterday_tasks),
        'today_tasks': list(today_tasks),
        'tomorrow_tasks': list(tomorrow_tasks),
        'scheduled_tasks': list(scheduled_tasks),
        'form': form}
    return render(request, 'home.html', context=context)


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
            return render(request, 'task.html', {'task': task})
        else:
            task.is_completed = True
            task.save()
            return render(request, 'task.html', {'task': task})
    else:
        return HttpResponseForbidden()


@login_required()
def delete_task(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        if task.user == request.user:
            task.delete()
            messages.success(request, 'Task deleted successfully.')
            return redirect('home')
    return HttpResponseForbidden()


@login_required()
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskAddFrom(request.POST, instance=task)
        if form.is_valid():   
            form.save()
            return render(request, 'task.html', {'task': task})
    form = TaskAddFrom(instance=task)
    return render(request, 'edit_task_modal.html', {'form': form})
