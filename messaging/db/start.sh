#!/bin/bash

set -x
source /ENV
/django-project/manage.py runserver 0.0.0.0:8000
