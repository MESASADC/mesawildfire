#!/bin/bash

# Django 1.4.x and earlier does not work with current ubuntu packages
# for libgeos. A ticket for the issue has been logged here: 
# https://code.djangoproject.com/ticket/20036 
# but Django 1.4.5 is in security fixes only mode, so has not been fixed
# The patch can be applied as follows:

sed -i "/\$.*/ {N; s/\$.*def geos_version_info/\.\*\$\'\)\ndef geos_version_info/g}" venv/lib/python2.7/site-packages/django/contrib/gis/geos/libgeos.py

# This gist explains how to patch libgeos, as an alternative: 
# https://gist.github.com/fission6/7619954
# This requires building libgeos from source
