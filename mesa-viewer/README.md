# AFIS Viewer

This is the repository for the AFIS web frontend django application.

## Prerequisites:

* It is assumed you have docker (http://docker.com) installed and are familiar
  with its usage, and that you are in the docker group on your host OS
* It is assumed you have git installed and are familiar with its usage
* You need to have access to either the kartoza.com or Meraka private git repos
 (lets assume you have that if you are reading this!).


**host**: Always refers to the host production or development server.
**image**: A deployable virtualised application image.
**container**: A deployed virtualised application instance.

## Docker setup:

### Postgis image creation:

This is only needed for developers wanting to use a testing version
of the AFIS postgis database. You need to have a sample dump - contact 
Riaan van den Dool for this if needed.

#### Method 1 (for the bandwidth constrained / impatient):

We will build the postgis image using apt-cacher-ng debian package caching:

On the host:

```
sudo apt-get install apt-cacher-ng
git clone https://github.com/kartoza/docker-postgis
cd docker-postgis
vim 71-apt-cacher-ng
```

At this point you should add a line with your host IP address (don't use
localhost or 127.0.0.1, it must be routable from inside the container).

For example:

```
Acquire::http { Proxy "http://192.168.1.1:3142"; };
```

Now continue to build the postgis image:

```
./build.sh
```


#### Method 2 (for the keyboard impaired):

```
docker build -t kartoza/postgis git://github.com/kartoza/docker-postgis.git
```


At this point you should now have a postgis image available to you:

```
docker images
```

Should show something like this:

```
REPOSITORY          TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
kartoza/postgis     latest              b9baae02c47f        15 minutes ago      474.5 MB
```

### Postgis Container Setup

Now we need to bring up and load data into the postgis container.


```
docker run --name="afis-postgis" -d -t kartoza/postgis
```

**Note:** that there is a 10 second wait while the databases initialise.

Now determine the IP address of the running container and then
restore the dump to it. I use the ``dipall`` script provided 
[here](https://github.com/kartoza/docker-helpers) to easily
determine the IP address.

Also you need to have the ``postgresql-client-9.3`` package installed
to use the following command:

```
pg_restore afisapps-20140725.Fc.dmp | psql -h <ipaddress> -U docker gis
```

(Replace ``ipaddress`` with the appropriate IP address from ``dipall``)

Finally you also need to modify the docker db role so that it includes
the viewer, common and postgis schemas:

```
echo "ALTER ROLE docker SET search_path=viewer, common, postgis;" | \
    psql -h <ipaddress> -U docker gis
```

## Virtualenv setup
 
 
### Install requirements

In the top level dir of this repo do:

```
bash
virtualenv venv
source venv/bin/activate
pip install -r REQUIREMENTS.txt
```

**Note:** I prefer using straight virtualenv to work_on etc.

### Patch geos

The version of geos provided by pip is not compatible with django 1.4 so you
need to patch it as follows:

```
sed -i "/\$.*/ {N; s/\$.*def geos_version_info/\.\*\$\'\)\ndef geos_version_info/g}" \
    venv/lib/python2.7/site-packages/django/contrib/gis/geos/libgeos.py
```

## Create a development settings file

Create a simple settings file in ``django_project/settings/dev_<your_name>.py``
 
```
python

from afis_web_basic import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'gis',
        'USER': 'docker',
        'PASSWORD': 'docker',
        'HOST': '172.17.0.57',
        'PORT': 5432,
        # Name to be used for unit testing db
        'TEST_NAME': 'afis-test',
    },
}
```

If you have followed the setup process above, probably you only need to 
change the IP address of your docker container.

## Create a test user

If you want to create a test user you can do it as follows (ensure that the
virtualenv is activated first):

```
bash
cd django_project
python manage.py \
    createsuperuser \
    --username=docker \
    --email=test2@test.com \
    --settings=settings.dev_werner
```

## Using Django syncdb

If you are not using a database dump, then you might encounter an error while trying to syncdb:
```
django.db.utils.DatabaseError: relation "auth_user" does not exist
LINE 1: ...ser"."last_login", "auth_user"."date_joined" FROM "auth_user...
```

A workaround for this error is to comment out the 'afisweb' django app in settings/afis_web_basic.py
until after you have run syncdb for the first time

Also, make sure that you do not set the schema search path as described above if you are not using
a database dump that hase these schemas set up already. To set the search path back to the default 'public':

```
echo "ALTER ROLE docker SET search_path=public;" | \
    psql -h <ipaddress> -U docker gis
```


## Using the Docker provided

Before doing this, make sure you have the afis-postgis docker running and that you have run the init_db script in the ``django_project`` folder.

###First, we will build the docker using our build script in the root directory.
```
env IMAGE_NAME=<image_name> ./build //Default is "afis-viewer"
```

###Next, we will run the docker, but this will need some configuration.

Before we do that we have to tell nginx that we want our app to be hosted.

If you already have nginx set up, simply go to ``/etc/nginx/sites-available/``.
Create a file named `afis-viewer`, and enter the following content:
```
server {
	listen 20080; // The port of your choice
    #server_name afisviewer; //Name of your choice
    location /static {
    	alias /dir/to/afis-viewer/static_root; //Actual location of our static files
        autoindex off;
    }
    location / {
    	include /dir/to/afis-viewer/runtime/uwsgi_params;
        uwsgi_pass unix:/dir/to/afis-viewer/runtime/uwsgi.sock;
    }
}
```
Now, create a sym-link to the sites-enabled folder and restart nginx:
```
sudo ln -s /etc/nginx/sites-available/afis-viewer /etc/nginx/sites-enabled/
sudo service nginx reload
```

>In the ``afis-viewer/runtime/start.sh`` as identified at the end of the Dockerfile, make sure that the correct static file folder is copied to the correct mounted directory e.g:
```
cp -r /opt/django_project/afisweb/static/* /mnt/static
```
Also, make sure the log file is created and permissions are added, since it is referenced in ``django_project/settings/afis_web_basic.py``, e.g.
```
mkdir -p /opt/logs && touch /opt/logs/mylog.log && chmod -R ugo+rw /opt/logs
```

>In the  runtime/uwsgi.ini, make sure that the socket permissions are set to 666, and set the ``DJANGO_SETTINGS_MODULE`` to settings.dev_(your_name).



Here are a few environment variables we have to take into account:

 ``RUN_MODE``:
>``DAEMON``: Will run docker as a Daemon.
>``INTERACTIVE``: Will run the docker verbosely
 
``USER``:The user to perform this task *[Default: "root"]* .
``RUN_NAME``:The name of our docker image *[Default: "afis-viewer"]* .
``IMAGE_NAME``: The name of our docker image *[Default: "afis-viewer"]*.
``AFIS_VIEWER_DATABASE_NAME``: The name of the database running in the afis-postgres docker *[Preferred: "gis"]* .
``AFIS_VIEWER_DATABASE_USER``: The username of the database running in the afis-postgres docker *[Preferred: "docker"]*.
``AFIS_VIEWER_DATABASE_PASS``: The password of the database running in the afis-postgres docker *[Preferred: "docker"]*.
``AFIS_VIEWER_DATABASE_HOST``: The IP address of the docker of the database running in the afis-postgres docker *[Suggested: "0.0.0.0"]*.
``AFIS_VIEWER_DATABASE_PORT``:  The port on the IP of the database running in the afis-postgres docker *[Suggested: "15432"]*.
``AFIS_VIEWER_STATIC_ROOT``: The location of the static files within the docker *[Preferred: "/mnt/static"]*.

Finally, run the docker using the run script and inject the above mentioned environment variables.

```
docker rm afis-viewer;
env USER=root RUN_MODE=INTERACTIVE RUN_NAME=werner-viewer IMAGE_NAME=werner-viewer AFIS_VIEWER_DATABASE_NAME=gis AFIS_VIEWER_DATABASE_USER=docker AFIS_VIEWER_DATABASE_PASS=docker AFIS_VIEWER_DATABASE_HOST=<My IP Address> AFIS_VIEWER_DATABASE_PORT=15432 AFIS_VIEWER_STATIC_ROOT=/mnt/static ./run
```