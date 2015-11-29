import os
import sys

WSGI_DIR = os.path.dirname(__file__)
path1 = os.path.join(WSGI_DIR, '..')
path2 = os.path.join(WSGI_DIR, '..', 'django_project')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
sys.path.append( path1 )
sys.path.append( path2 )

