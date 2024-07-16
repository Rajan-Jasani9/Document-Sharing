from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.register_login , name='register_login'),
    path('login', views.login_user , name='login_user'),
    path('register', views.register , name='register'),
]
