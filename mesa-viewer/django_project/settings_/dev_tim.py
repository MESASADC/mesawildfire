# noinspection PyUnresolvedReferences
from afis_web_full import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'gis',
        'USER': 'docker',
        'PASSWORD': 'docker',
        'HOST': '172.17.0.57',
        'PORT': 5432,
        # Name to be used for unit testing db
        'TEST_NAME': 'afis-test',
    },
}
