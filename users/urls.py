from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('login', views.UserLoginView.as_view()),
    # path('register')
]
