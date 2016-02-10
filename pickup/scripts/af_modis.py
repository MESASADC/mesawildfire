#!/usr/bin/env python
# -*- coding: utf-8 -*-


from jinja2 import Environment, FileSystemLoader;
import sys, os
import logging
from kombu import Connection, Exchange, Queue
import datetime
import json


def render_message_payload(template_dir, template_name, **kwargs):
    #logging.debug('Template variables: %s' % str(kwargs)) 
    loader = FileSystemLoader(template_dir);
    env = Environment(loader=loader);
    template = env.get_template(template_name);
    return template.render(**kwargs)

script_dir = os.path.dirname(sys.argv[0])
incron_dir = sys.argv[1]
incron_file = sys.argv[2]
incron_filepath = os.path.join(incron_dir, incron_file)
incron_event = sys.argv[3]

logfile = os.path.join(script_dir, 'af_modis.log')
#logfile='/dev/stdout'
logging.basicConfig(filename=logfile,level=logging.DEBUG, format='%(asctime)s :: %(message)s')

configfile = os.path.join(script_dir, 'config.json')
config = json.loads(open(configfile).read())

uri = 'amqp://{amqp_user}:{amqp_pass}@{amqp_host}:{amqp_port}/{amqp_vhost}'.format(**config)

try:

    logging.info('Processing: {}/{} for {}'.format(incron_dir, incron_file, incron_event))
    logging.info('Trying to establish AMQP connectiion: %s' % uri)
    
    # Connect to rabbitmq server
    with Connection(uri) as conn:
        conn.connect()
        logging.info('Connection established: %s' % uri)
        exchange = Exchange(config['amqp_exchange'], type='topic', channel=conn.default_channel)
        exchange.declare()
        count = 0
        for line in open(incron_filepath):
            # Compose message payload
            lat, lon, btemp, frp, res, MM_DD_YYYY, HHMM, sat, confidence = line.split(',')
            YYYY_MM_DD = "{}-{}-{}".format(MM_DD_YYYY[6:10], MM_DD_YYYY[0:2], MM_DD_YYYY[3:5])
            HH_MM_SS = "{}:{}:00".format(HHMM[:2], HHMM[2:4])
            body = render_message_payload(script_dir, "af_modis_template.json", id='null', src='CSIR', lon=lon, lat=lat, btemp=btemp, frp=frp, YYYY_MM_DD=YYYY_MM_DD, HH_MM_SS=HH_MM_SS, sat=sat, confidence=confidence)
            #logging.debug(body)
            # Publish message
            rk = 'af_modis.m01.0.0.1.1'
            exchange.publish(body, rk)
            count += 1
            #logging.debug('Published a message with rk: %s' % rk)
        logging.info('Published %d af_modis messages' % count)
    logging.info('Deleting succesfully processed file: %s' % incron_filepath)
    #os.remove(incron_filepath)
except:
    logging.exception('Failed to process: {}/{} for {}'.format(incron_dir, incron_file, incron_event))


