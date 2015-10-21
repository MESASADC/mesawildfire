Admin scripts
=============


Installation on a vanilla Ubuntu OS. 
------------------------------------

Recommended: Ubuntu Desktop 14.04 64-bit

**Step 1: Preparation:**

***Option 1***

Copy the contents of the ./admin/ directory in this repo to the target machine.

***Option 2***

Start by cloning the whole repo to the target machine:

<pre>
    $ sudo apt-get install git
    $ git clone https://github.com/MESASADC/mesawildfire.git
    $ chmod +x ./mesawildfire/admin/install
</pre>

**Step 2: Install the Wildfire software and its dependencies:**

<pre>
    $ cd ./mesawildfire/admin/
    $ sudo ./install
</pre>


Starting up:
------------

The Docker containers are managed by Supervisord.

Supervisord should start up automatically when the computer boots up.

Manual procedure:
<pre>
    $ sudo service start supervisor
    $ sudo service status supervisor
</pre>


Checking the status of the system:
----------------------------------

*Docker:*
<pre>
    $ sudo docker ps
</pre>

*Supervisord:*

<pre>
    $ sudo service supervisor status
</pre>

or open in your browser: http://localhost:9090/

*Logs:*
<pre>
    $ sudo tail -f /var/log/supervisor/*
</pre>

or click on application names in your browser: http://localhost:9090/

