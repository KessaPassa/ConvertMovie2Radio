from django.urls import path

from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('redirect', views.redirect, name='redirect'),
]