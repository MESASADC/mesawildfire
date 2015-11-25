from django.conf.urls.defaults import *
from afisweb.views import *
# enable the admin interface:
from django.contrib import admin
from django.conf import settings

admin.autodiscover()
urlpatterns = patterns(
    '',
    ('', include('registration_backends.custom.urls')),
    # Required when using Django manage.py runserver
    ( r'^static/(?P<path>.*)$', 'django.views.static.serve',
      {'document_root': settings.STATIC_ROOT, 'show_indexes': True} ),
    (r'^admin/', include(admin.site.urls)),
    # For our landing page
    ( r'^$', landingPage ),
    # Expose next_page parameter
#    ( r'^logout/?next=(?P<next_page>.*)$', 'django.contrib.auth.views.logout'),
    ( r'^addBackdropLayers.js$', addBackdropLayers ),
    ( r'^addDataLayers.js$', addDataLayers ),
    ( r'^showLegend/$', showLegend ),
    ( r'^showFireStats/$', showFireStats ),
    ( r'^showLayerManager/$', showLayerManager ),
#    ( r'^show-contact-form/$', show_contact_form ),
#    ( r'^send-user-message/$', send_user_message ),
    ( r'^fpasld.xml$', fireProtectionAgencySLD ),
    ( r'^help/$', help ),
    ( r'^disclaimer/$', disclaimer ),
    ( r'^dateQuery/$', dateQuery ),
    ( r'^places/$', places),
    ( r'^baseLayerDialog/$', baseLayerDialog),
    ( r'^setLayerVisibility/(?P<theId>\d+)/(?P<theFlag>[t]|[f])/$', setLayerVisibility ),
    ( r'^saveLegend/(?P<theId>\d+)/(?P<theOrder>\d+)/(?P<theDeletedState>[t]|[f])/$', saveLegend ),
    ( r'^setLayerDeletedState/(?P<theId>\d+)/(?P<theDeletedFlag>[t]|[f])/(?P<theVisibleFlag>[t]|[f])/$', setLayerDeletedState ),
    ( r'^getPlaceNames/$', getPlaceNames ),
    ( r'^uploadFeature/$', uploadFeature),
#    ( r'^partners/$', partners),
    ( r'^getFeatureInfo/(?P<theLon>[-]*\d+.\d+)/(?P<theLat>[-]*\d+.\d+)/(?P<theBoundingBox>[0-9\-,.]*)/(?P<thePixelX>\d+)/(?P<thePixelY>\d+)/(?P<theMapWidth>\d+)/(?P<theMapHeight>\d+)/(?P<theMapScale>\d+\.\d+)/$', getFeatureInfo),
#    ( r'^getFireReport/', getFireReport),
    ( r'^updateOpenLayerStrings/$', updateOpenLayerStrings ),
    ( r'^getWildcardSubDomainInfo/$', get_wildcard_sub_domain_info ),

    # Workaround to fetch swath image from mapserver on a different server
    ( r'^mapserv/(?P<params>.+)', redirect_mapserver_request ),

    #20120503 zoom in to a specific lat,lon
    #( r'^(?P<latlong>.+)$', landingPage ),
)
