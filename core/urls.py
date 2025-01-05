from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('create_task/', views.create_task, name='create_task'),
    path('check_task/<int:task_id>/', views.check_task, name='check_task'),
]