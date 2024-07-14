from django.contrib import admin
from django.urls import path, include
from .views import register_login


urlpatterns = [
    path('', register_login , name='register_login'),
]
