# Django settings

DEBUG = False
 
import os
import re
from middleware.stripwhitespace import StripWhitespaceMiddleware

try:
  from settings_nogit import CMDLINE_FES, CMDLINE_OPENAFIS
except:
  print "File not found: settings_nogit.py"

LOCAL_JQUERY=True
LOCAL_OPENLAYERS=True
USE_GOOGLE=True # Set to False for debugging. 
AFIS_WMS_URL = 'http://afis.meraka.org.za/geoserver/wms'

#Used for fetching firestats
AFIS_WFS_URL = 'http://afis.meraka.org.za/geoserver/wfs'
AFIS_MAPSERVER_URL = 'http://afis.meraka.org.za/cgi-bin/mapserv'

# Keep users logged in for as long as possible 
SESSION_EXPIRE_AT_BROWSER_CLOSE=False
SESSION_COOKIE_AGE=31536000 # one year

ROOT_PROJECT_FOLDER = os.path.dirname(__file__)

# We previously added these two lines
# When setting up project wide templates
MEDIA_ROOT = os.path.join(ROOT_PROJECT_FOLDER,'static')
MEDIA_URL = '/static/'

# directory where to store cached asLegend images
LEGEND_IMAGE_ROOT = os.path.join(MEDIA_ROOT, 'images','legend')
LEGEND_IMAGE_URL = os.path.join('/static', 'images','legend')
if not os.path.exists(LEGEND_IMAGE_ROOT):
    os.makedirs(LEGEND_IMAGE_ROOT) and os.chmod(LEGEND_IMAGE_ROOT, 0777)


#add trailing slash to urls
APPEND_SLASH=True

# Which clients may receive debug messages...
INTERNAL_IPS = ('127.0.0.1')

# Also added for logging disabled for prod machine
TEMPLATE_DEBUG = DEBUG
LOGGING_OUTPUT_ENABLED=DEBUG
LOGGING_LOG_SQL=DEBUG

ADMINS = (
    ('Cheewai Lai', 'clai@csir.co.za'),
    ('Riaan van den Dool', 'rvddool@csir.co.za'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
      'ENGINE' : 'postgresql_psycopg2', 	
      'NAME' : os.environ['AFIS_VIEWER_DATABASE_NAME'],
      'USER' : os.environ['AFIS_VIEWER_DATABASE_USER'],
      'PASSWORD' : os.environ['AFIS_VIEWER_DATABASE_PASS'],
      'HOST' : os.environ['AFIS_VIEWER_DATABASE_HOST'],
      'PORT' : os.environ['AFIS_VIEWER_DATABASE_PORT'],
      # Name to be used for unit testing db
      'TEST_NAME' : 'afis-test',            
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

# Make this unique, and don't share it with anybody.
SECRET_KEY = '8q0qjt=01sg-0bz6wc_(kh3i5wfb*!kv2qr8k_6^h5^b4&)8)1'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'middleware.stripwhitespace.StripWhitespaceMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.csrf.CsrfResponseMiddleware',
    # Added by Tim for advanced loggin options
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # Dont use this it will break template rendered html
    #'middleware.prettify.PrettifyMiddleware',
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
    os.path.join(ROOT_PROJECT_FOLDER, '../../python/lib/python2.7/site-packages/debug_toolbar/templates/debug_toolbar'),
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

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'registration',
    'debug_toolbar',
    # add these two lines for admin
    'django.contrib.admin',
    'django.contrib.gis',
    # afis-viewer app
    'afisweb',
    # afis single-signon shared models
    'common',
)

CUSTOM_WILDCARD_SUBDOMAIN_INFO = { 
  'us' : { None: { 'west': -130.0, 'south': 25.0, 'east': -70.0, 'north': 50.0 } }, 
  'uk' : { None: { 'west': -9.0, 'south': 49.0, 'east': 2.0, 'north': 59.0 }, 
           '*': 'gb',  # This maps *.uk.afis.co.za to *.gb.afis.co.za
         }, 
  'ru' : { None: {"west": 22.0, "south": 41.0, "east": 180, "north": 82.0} }, 
  'ca' : { None: {"west": -141.0, "south": 41.0, "east": -53.0, "north": 70.0} }, 

  }

#20111104 clai http://stackoverflow.com/questions/5438642/django-setup-default-logging
'''
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(ROOT_PROJECT_FOLDER, '/mnt/runtime/logs/mylog.log'),
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },  
        'request_handler': {
                'level':'DEBUG',
                'class':'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(ROOT_PROJECT_FOLDER, '/mnt/runtime/logs/django_request.log'),
                'maxBytes': 1024*1024*5, # 5 MB
                'backupCount': 5,
                'formatter':'standard',
        },
    },
    'loggers': {

        '': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True
        },
        'django.request': { # Stop SQL debug from logging to main logger
            'handlers': ['request_handler'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}
'''
