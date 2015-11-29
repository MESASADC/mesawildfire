FROM ubuntu:14.04

MAINTAINER rvddool@csir.co.za

ENV DEBIAN_FRONTEND noninteractive

RUN sed 's/main$/main universe multiverse/' -i /etc/apt/sources.list
RUN apt-get update

# install uwsgi first because it takes quite a while
RUN apt-get install -y build-essential python python-dev python-setuptools
RUN easy_install pip
RUN pip install uwsgi

# install additional packages
RUN apt-get install -y postgresql-client libpq-dev libgeos-c1 nano vim

# install python requirements specified in REQUIREMENTS.txt
# using template for loop to avoid using ADD
RUN pip install django==1.4.5
RUN pip install django-registration==0.8
RUN pip install django-debug-toolbar==1.2.2
RUN pip install django-extensions==1.4.6
RUN pip install psycopg2==2.5.4
RUN pip install simplejson==3.6.5
RUN pip install googlemaps==1.0.2
RUN pip install PyYAML==3.11
RUN pip install django-analytical==0.19.0

# Patch GeoDjango 1.4: https://code.djangoproject.com/ticket/20036
RUN sed -i "/\$.*/ {N; s/\$.*def geos_version_info/\.\*\$\'\)\ndef geos_version_info/g}"  /usr/local/lib/python2.7/dist-packages/django/contrib/gis/geos/libgeos.py

EXPOSE 8000

# Run CMD as RUN_USER to avoid security issues
ENTRYPOINT ["/tmp/runtime/runuser.sh"]
CMD ["/tmp/runtime/start.sh"]