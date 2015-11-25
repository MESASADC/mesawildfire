from afis_web_basic import *
import os

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.environ.get('AFIS_VIEWER_DATABASE_NAME', 'gis'),
        'USER': os.environ.get('AFIS_VIEWER_DATABASE_USER', 'docker'),
        'PASSWORD': os.environ.get('AFIS_VIEWER_DATABASE_PASS', 'docker'),
        'HOST': os.environ.get('AFIS_VIEWER_DATABASE_HOST', 'afis-postgis'),
        'PORT': os.environ.get('AFIS_VIEWER_DATABASE_PORT', 5432),
        # Name to be used for unit testing db
        'TEST_NAME': 'afis-test',
    },
}


