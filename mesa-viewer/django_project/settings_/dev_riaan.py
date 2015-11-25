from afis_web_basic import *

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'gis',
        'USER': 'docker',
        'PASSWORD': 'docker',
        'HOST': '127.0.0.1',
        'PORT': 15432,
        # Name to be used for unit testing db
        'TEST_NAME': 'afis-test',
    },
}


