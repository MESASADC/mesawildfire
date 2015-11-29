#!/bin/bash

# initialize the database using syncdb
cd /tmp/django_project/
export AFIS_VIEWER_INIT=True
python manage.py syncdb --settings=$DJANGO_SETTINGS_MODULE

unset AFIS_VIEWER_INIT
python manage.py syncdb --settings=$DJANGO_SETTINGS_MODULE
