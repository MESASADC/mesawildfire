#!/bin/bash

# Configure supervisord for field terminal use
# See: http://serverfault.com/questions/96499/how-to-automatically-start-supervisord-on-linux-ubuntu

apt-get install -y supervisor

cp init.d/supervisord /etc/init.d/supervisord
chmod +x /etc/init.d/supervisord

cp conf.d/* /etc/supervisor/conf.d/

update-rc.d supervisord defaults

service supervisord stop
service supervisord start
service supervisord status








