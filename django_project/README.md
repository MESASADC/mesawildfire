MESA Django Application
=======================

Consists of django apps:

* REST interface
* AMQP messaging backend

To build:

    $ ./build

To configure:

    $ cp ENV.example ENV
    $ nano ENV

To start REST interface:

    # Requires PostGIS DB at connections details as in ENV
    # Requires RabbitMQ at connections details as in ENV
    
    # First time, or after django model updates:
    ./run /django_project/manage.py migrate
    
    # Otherwise:
    ./run
    
To start AMQP backend:

    ./run /django_project/manage.py mesa_comms
   
