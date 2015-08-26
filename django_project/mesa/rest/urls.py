from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from mesa.rest import views


router = routers.DefaultRouter()
router.register(r'ConfigSetting', views.ConfigViewSet)
router.register(r'FdiPoint', views.FdiPointViewSet)
router.register(r'FdiMeasurement', views.FdiMeasurementViewSet)
router.register(r'FdiForecast', views.FdiForecastViewSet)
router.register(r'FdiPointData', views.FdiTableViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns += format_suffix_patterns([
    #url(r'^$', views.api_root),
    url(r'^af_modis/$',
        views.AfModisList.as_view(),
        name='af_modis-list'),
    url(r'^af_modis/(?P<pk>[0-9]+)/$',
        views.AfModisDetail.as_view(),
        name='af_modis-detail')
])


# http://www.django-rest-framework.org/tutorial/quickstart/

"""
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views

# API endpoints
urlpatterns = format_suffix_patterns([
    url(r'^$', views.api_root),
    url(r'^snippets/$',
        views.SnippetList.as_view(),
        name='snippet-list'),
    url(r'^snippets/(?P<pk>[0-9]+)/$',
        views.SnippetDetail.as_view(),
        name='snippet-detail'),
    url(r'^snippets/(?P<pk>[0-9]+)/highlight/$',
        views.SnippetHighlight.as_view(),
        name='snippet-highlight'),
    url(r'^users/$',
        views.UserList.as_view(),
        name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$',
        views.UserDetail.as_view(),
        name='user-detail')
])

# Login and logout views for the browsable API
urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]
"""
