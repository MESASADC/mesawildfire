# Django settings for the basic AFIS Viewer web application
# hosted at Meraka

from afis_web_basic import *

# Debug settings
DEBUG = False
TEMPLATE_DEBUG = DEBUG
LOGGING_OUTPUT_ENABLED = DEBUG
LOGGING_LOG_SQL = DEBUG

# Which clients may receive debug messages...
INTERNAL_IPS = ('127.0.0.1')

# a list of one or more proxies to use for server side
# web requests (e.g. getfeatureinfo) via urllib
# set to None to use environment var settings or no proxy
# example: PROXIES={'http': 'http://proxy.meraka.csir.co.za:3128'}
PROXIES=None

# For django registration
EMAIL_HOST = 'smtp.csir.co.za'
DEFAULT_FROM_EMAIL = 'noreply@afis.co.za'

POSTGIS_VERSION = (2, 1, 5)



