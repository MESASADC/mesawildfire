from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from mesa.rest import views

router = routers.DefaultRouter()
router.register(r'ConfigSetting', views.ConfigViewSet)
router.register(r'FdiPoint', views.FdiPointViewSet)
router.register(r'FdiMeasurement', views.FdiMeasurementViewSet)
router.register(r'FdiForecast', views.FdiForecastViewSet)
router.register(r'FdiPointData', views.FdiPointDataViewSet)
router.register(r'FireEvent', views.FireEventViewSet, base_name='FireEvent')
router.register(r'FirePixel', views.FirePixelViewSet)
router.register(r'FireFeature', views.FireFeatureViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

