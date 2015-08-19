#!/bin/bash

set -x
source /ENV

if [ $# -eq 0 ]; then
    # No arguments provided
    /django_project/manage.py runserver 0.0.0.0:8000
else
    $*
fi

