# resume_builder/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.resume_create, name='index'),
]

