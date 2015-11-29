#!/bin/bash

# create legend images directory
mkdir -p /tmp/django_project/static_root/images/legend

# collect static files into the project static dir
# http://blog.doismellburning.co.uk/2012/06/25/django-and-static-files/
#cd /opt/django_root/ && python manage.py collectstatic
cp -r /tmp/django_project/afisweb/static/* /tmp/django_project/static_root/

# run supervisord to manage the uwsgi process
#supervisord --nodaemon --configuration /mnt/runtime/supervisord.conf

# keep running uwsgi in a loop, crude way of restarting on a crash
#while true; do
#    /usr/local/bin/uwsgi --ini /tmp/runtime/uwsgi.ini
#done
