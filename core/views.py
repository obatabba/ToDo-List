from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.shortcuts import render
from .models import Task


class Login(LoginView):
    template_name = 'login.html'


class Logout(LogoutView):
    next_page = 'home'
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "You have been logged out successfully.")
        return super().dispatch(request, *args, **kwargs)


def home(request):
    tasks = Task.objects.all()
    return render(request, 'home.html', {'tasks': list(tasks)})