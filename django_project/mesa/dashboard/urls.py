from django.conf.urls import include, url
from django.contrib import admin
from mesa.dashboard import views

urlpatterns = [
    url(r'^', views.dashboard, name='dashboard'),
]

