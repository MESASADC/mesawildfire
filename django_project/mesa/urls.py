
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('mesa.home.urls')),
    url(r'^rest/', include('mesa.rest.urls')),
    url(r'^dashboard/', include('mesa.dashboard.urls')),
]

