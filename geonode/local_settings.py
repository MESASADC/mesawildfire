import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

SITEURL = "http://localhost:8111/"

DATABASES = {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': utils.get_env('GEONODE_DB_NAME'),
        'USER': utils.get_env('GEONODE_DB_USER'),
        'PASSWORD': utils.get_env('GEONODE_DB_PASS'),
        'HOST': utils.get_env('GEONODE_DB_HOST'),
        'PORT': utils.get_env('GEONODE_DB_PORT'),
        # Name to be used for unit testing db
        'TEST_NAME': 'afis-test',    
     },
    # vector datastore for uploads
    'datastore' : {
        'ENGINE': 'django.contrib.gis.db.backends.postgis', # Empty ENGINE name disables 
        'NAME': utils.get_env('GEONODE_DB_NAME'),
        'USER': utils.get_env('GEONODE_DB_USER'),
        'PASSWORD': utils.get_env('GEONODE_DB_PASS'),
        'HOST': utils.get_env('GEONODE_DB_HOST'),
        'PORT': utils.get_env('GEONODE_DB_PORT'),
    }
}

# OGC (WMS/WFS/WCS) Server Settings
OGC_SERVER = {
    'default' : {
        'BACKEND' : 'geonode.geoserver',
        'LOCATION' : 'http://localhost:8080/geoserver/',
        'PUBLIC_LOCATION' : 'http://localhost:8080/geoserver/',
        'USER': utils.get_env('GEONODE_OGC_USER'),
        'PASSWORD': utils.get_env('GEONODE_OGC_PASS'),
        'MAPFISH_PRINT_ENABLED' : True,
        'PRINT_NG_ENABLED' : True,
        'GEONODE_SECURITY_ENABLED' : True,
        'GEOGIG_ENABLED' : True,
        'WMST_ENABLED' : True,
        'BACKEND_WRITE_ENABLED': True,
        'WPS_ENABLED' : True,
        'LOG_FILE': '%s/geoserver/data/logs/geoserver.log' % os.path.abspath(os.path.join(PROJECT_ROOT, os.pardir)),
        # Set to name of database in DATABASES dictionary to enable
        'DATASTORE': '', #'datastore',
    }
}

CATALOGUE = {
    'default': {
        # The underlying CSW implementation
        # default is pycsw in local mode (tied directly to GeoNode Django DB)
        'ENGINE': 'geonode.catalogue.backends.pycsw_local',
        # pycsw in non-local mode
        # 'ENGINE': 'geonode.catalogue.backends.pycsw_http',
        # GeoNetwork opensource
        # 'ENGINE': 'geonode.catalogue.backends.geonetwork',
        # deegree and others
        # 'ENGINE': 'geonode.catalogue.backends.generic',

        # The FULLY QUALIFIED base url to the CSW instance for this GeoNode
        'URL': '%scatalogue/csw' % SITEURL,
        # 'URL': 'http://localhost:8080/geonetwork/srv/en/csw',
        # 'URL': 'http://localhost:8080/deegree-csw-demo-3.0.4/services',

        # login credentials (for GeoNetwork)
        'USER': utils.get_env('GEONODE_CSW_USER'),
        'PASSWORD': utils.get_env('GEONODE_CSW_PASS'),
    }
}

# Default preview library
#LAYER_PREVIEW_LIBRARY = 'geoext'
