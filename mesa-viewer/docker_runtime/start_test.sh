#!/bin/bash

# static files are handled by django.views.static.serve
cd /tmp/django_project/
python manage.py runserver --settings=$DJANGO_SETTINGS_MODULE 0.0.0.0:8000
