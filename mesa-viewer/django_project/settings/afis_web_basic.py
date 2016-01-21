# Django settings for the basic AFIS Viewer web application
# with less dependencies than the full production deployment

# Debug settings
DEBUG = True
TEMPLATE_DEBUG = DEBUG
LOGGING_OUTPUT_ENABLED = DEBUG
LOGGING_LOG_SQL = DEBUG

# Which clients may receive debug messages...
INTERNAL_IPS = ('127.0.0.1')

ADMINS = (
    ('Cheewai Lai', 'clai@csir.co.za'),
    ('Riaan van den Dool', 'rvddool@csir.co.za'),
)

import os

# Import secret key randomly generated by utils.py
import utils
from secret_key import *

# Defaults, to get code to run. Override in afis_web_full.py for production.
FIRE_STATS_MODIS = []

LOCAL_JQUERY=True
LOCAL_OPENLAYERS=True
USE_GOOGLE=True # Set to False for debugging.
HQ_GEOSERVER_URL = 'http://afis.meraka.org.za/geoserver/'
GEOSERVER_URL = utils.get_env('AFIS_VIEWER_GEOSERVER_URL') or HQ_GEOSERVER_URL
AFIS_WMS_URL = GEOSERVER_URL +'wms'

# Keep users logged in for as long as possible
SESSION_EXPIRE_AT_BROWSER_CLOSE=False
SESSION_COOKIE_AGE=31536000 # one year

ROOT_PROJECT_FOLDER = os.path.join(os.path.dirname(__file__), '..')

# collectstatic will look in each app dir for <APP>/static and
# collect the resources all up to django_project/static_root (which should not be
# under VCS)
STATIC_ROOT = os.environ.get(
    'AFIS_VIEWER_STATIC_ROOT', os.path.join(ROOT_PROJECT_FOLDER, 'static_root'))
STATIC_URL = '/static/'

# Some files refer to MEDIA_ROOT or MEDIA_URL, so just do this for now:
MEDIA_ROOT = os.environ.get(
    'AFIS_VIEWER_MEDIA_ROOT', os.path.join(ROOT_PROJECT_FOLDER, 'media'))
MEDIA_URL = '/media/'

# directory where to store cached asLegend images
LEGEND_IMAGE_ROOT = os.path.join(STATIC_ROOT, 'images','legend')
LEGEND_IMAGE_URL = os.path.join('/static', 'images','legend')
if not os.path.exists(LEGEND_IMAGE_ROOT):
    os.makedirs(LEGEND_IMAGE_ROOT) and os.chmod(LEGEND_IMAGE_ROOT, 0777)


# a list of one or more proxies to use for server side
# web requests (e.g. getfeatureinfo) set to None to use environment var settings or no proxy
PROXIES=None


#add trailing slash to urls
APPEND_SLASH = True

# Used for javascript versioned urls
VERSION_STRING = os.environ.get('DEPLOYMENT', '123') + os.environ.get('RELEASE', '456')

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': utils.get_env('AFIS_VIEWER_DATABASE_NAME'),
        'USER': utils.get_env('AFIS_VIEWER_DATABASE_USER'),
        'PASSWORD': utils.get_env('AFIS_VIEWER_DATABASE_PASS'),
        'HOST': utils.get_env('AFIS_VIEWER_DATABASE_HOST'),
        'PORT': utils.get_env('AFIS_VIEWER_DATABASE_PORT'),
        # Name to be used for unit testing db
        'TEST_NAME': 'afis-test',
    },
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.

TIME_ZONE = 'Africa/Johannesburg'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'middleware.stripwhitespace.StripWhitespaceMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # Dont use this it will break template rendered html
    #'middleware.prettify.PrettifyMiddleware',
    # Added by Tim for advanced loggin options
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
)

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
    )

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(ROOT_PROJECT_FOLDER, 'templates'),
    )

# For django registration
ACCOUNT_ACTIVATION_DAYS = 2
EMAIL_HOST = 'localhost'
DEFAULT_FROM_EMAIL = 'noreply@afis.co.za'

#where to take the user after they logged in
LOGIN_REDIRECT_URL = '/'

#where to take the user if they try to access a page requiring a logged in user
LOGIN_URL = '/login/'

# Single-signon: All AFIS applications use the same user profile model:
AUTH_PROFILE_MODULE = 'common.UserProfile'

INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'registration',
    #'debug_toolbar',
    'django.contrib.admin',
    'django.contrib.gis',
    # afis-viewer app
    'afisweb',
    # afis single-signon shared models
    'common',
    # extras
    'analytical',
]

# Viewer running with Django < 1.4 cannot handle the newer default hasher, so default to SHA1
# https://docs.djangoproject.com/en/dev/topics/auth/passwords/
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)

# Loading data layers in Fern based deployments
FIXTURE_DIRS = [
   '/mnt/data/',
]

# Set AFIS_VIEWER_INIT=1 when running python manage syncdb the first time, to avoid error
if utils.get_env('AFIS_VIEWER_INIT'):
    INSTALLED_APPS.remove('afisweb')

import sys

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'stream': sys.stdout
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True
        },
    }
}

CUSTOM_LAYER = {
	'host':"//dashboard.mesa.afis.co.za/geoserver/wms",
	'namespace':"mesa",
	'layer_name':"custom_background"
}

GOOGLE_ANALYTICS_PROPERTY_ID = 'UA-72611319-1'


