from django.conf.urls import include, url
from django.contrib import admin
from mesa.home import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
]

