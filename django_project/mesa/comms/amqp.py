#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys, os
import logging
import kombu
from kombu import Connection, Exchange, Queue
from kombu.async import Hub
import datetime as dt
from functools import partial

from django.contrib.gis.geos import Point
from django.conf import settings
from mesa import models
import json

async = Hub()

logging.basicConfig(filename='/dev/stdout', format='%(levelname)s:    %(message)s', level=logging.DEBUG)


class ConsumingExchange(Exchange):

    def __init__(self, name, type_='topic', conn=None, channel=None, **kwargs):

        self.name = name
        self.type = type_
        self._conn = conn
        self._channel = channel
        self._conn_kwargs = {}
        self._queue_kwargs = {}
        self._consumer_producers = {}
        self._queues = []

        if type(self._conn) == str:
            # see if the conn parameter was a uri string
            try:
                self._conn = Connection(self._conn, **self._conn_kwargs)
            except Exception, e:
                logging.exception(e)
        if type(self._conn) is not Connection:
            raise ValueError('No valid connection available')

        self._conn.register_with_event_loop(async)

        if channel is None:
            # connection should provide a default channel
            self._channel = self._conn.default_channel

        super(ConsumingExchange, self).__init__(name=self.name, type=self.type, conn=self._conn, channel=self._channel, **kwargs)


    def bind_queue(self, queue=None, exchange=None, conn=None, channel=None, routing_keys=None, **kwargs):

        conn = conn or self._conn
        if type(conn) == str:
            # see if the conn parameter was a uri string
            try:
                conn = Connection(conn, **self._conn_kwargs)
            except Exception, e:
                logging.exception(e)
        if type(conn) is not Connection:
            raise ValueError('No valid connection available')
        conn.register_with_event_loop(async)

        if channel is None:
            # connection should provide a default channel
            channel = conn.default_channel

        if type(queue) == str:
            # see if the queue parameter was a name string
            try:
                queue = Queue(name=queue, channel=channel, **self._queue_kwargs)
            except Exception, e:
                logging.exception(e)
        if type(queue) is not Queue:
            raise ValueError('No valid queue available')

        queue.declare()
        queue.purge()

        logging.info("Binding queue '%s' to exchange '%s' with:" % (queue.name, exchange))
        routing_keys = routing_keys or ['#']
        for rk in routing_keys:
            try:
                logging.debug("rk: %s" % rk)
                queue.bind_to(exchange=exchange, routing_key=rk)
            except Exception, e:
                logging.exception(str(e))
        logging.info('Done: binding')

        consumer_tag = '%s::%s::consuming_exchange' % (self.name, queue.name)
        queue.consume(consumer_tag, callback=self._consumer_producer_callback, no_ack=True)

        self._queues.append(queue)
        return queue

    def _consumer_producer_callback(self, message):

        routing_key = message.delivery_info.get('routing_key')
        self.publish(message, routing_key)
        logging.info("Published a message with rk '%s' to '%s'" % (routing_key, self.name))
        return True
        
class BasePersistConsumer(Queue):
    
    def __init__(self, name, channel=None):
        
        self.connection = Connection(settings.MESA_FT_AMQP_URI)
        channel = channel or self.connection.default_channel
        super(BasePersistConsumer, self).__init__(name=name, channel=channel)

    def _consumer_callback(self, message):
        #logging.debug("callback %s", message.body)
        try:
            data = json.loads(message.body)
            self._persist(data)
        except ValueError, e:
            logging.exception(e)
            return True
        except Exception, e:
            logging.exception(e)
            return True
        return True

    def bind_queue(self, exchange=None, routing_keys=None, **kwargs):
        
        exchange = exchange or settings.MESA_FT_AMQP_EXCHANGE
        if type(exchange) == str:
            exchange = Exchange(exchange)

        logging.info("Binding persist queue '%s' to exchange '%s' with:" % (self.name, exchange.name))
        routing_keys = routing_keys or ['#']
        for rk in routing_keys:
            try:
                logging.debug("rk: %s" % rk)
                self.bind_to(exchange=exchange, routing_key=rk)
            except Exception, e:
                logging.exception(str(e))
        logging.info('Done: binding')
        consumer_tag = '%s::%s::persist' % (exchange.name, self.name)
        logging.debug("preconsume consumer_tag: {}".format(consumer_tag))
        self.consume(consumer_tag, callback=self._consumer_callback, no_ack=True)
        self.connection.register_with_event_loop(async)
        logging.debug("postconsume consumer_tag: {}".format(consumer_tag))
        return consumer_tag

    def _persist(self, message):
        raise NotImplementedError('Abstract method needs to be overridden')



class FirePixelPersistConsumer(BasePersistConsumer):


    def __init__(self, name, channel=None):
        
        self.translators =  {'af_modis': {
                                '0.1': self.af_modis
                            },
                            'af_viirs': {
                                '0.1': self.af_viirs
                            }}
        super(FirePixelPersistConsumer, self).__init__(name=name, channel=channel)


    def af_modis(self, data, obj):
        fields = data['fields']
        obj.type = data['type']
        obj.point = Point(*data['location']['geometry']['coordinates'])
        # approx pixel size in degrees 
        obj.vsize = 0.01
        obj.hsize = 0.01
        ddd = [int(v) for v in fields['date']['value'].split('-')]
        ttt = [int(v) for v in fields['time']['value'].split(':')]
        dddttt = ddd + ttt
        obj.date_time = dt.datetime(*dddttt )
        obj.src = fields['src']['value']
        obj.btemp = float(fields['btemp']['value'])
        obj.frp = float(fields['frp']['value'])
        obj.sat = fields['sat']['value']
        return obj

    def af_viirs(self, data, obj):
        fields = data['fields']
        obj.type = data['type']
        obj.point = Point(*data['location']['geometry']['coordinates'])
        # approx pixel size in degrees 
        obj.vsize = 0.005
        obj.hsize = 0.005
        ddd = [int(v) for v in fields['date']['value'].split('-')]
        ttt = [int(v) for v in fields['time']['value'].split(':')]
        dddttt = ddd + ttt
        obj.date_time = dt.datetime(*dddttt )
        obj.src = fields['src']['value']
        obj.btemp = float(fields['btemp']['value'])
        obj.frp = float(fields['frp']['value'])
        obj.sat = fields['sat']['value']
        return obj
                
    def _persist(self, data):
        try:
            #logging.info("FirePixel ".format(msg_type, msg_version))
            msg_type = data.get('type', None)
            if msg_type not in self.translators.keys():
                raise ValueError('Failed to persist: Unrecognized message type {0}'.format(repr(msg_type)))
            msg_version = data.get('version', None)
            if msg_version not in self.translators[msg_type].keys():
                raise ValueError('Failed to persist: Unrecognized message type version {0}:{1}'.format(repr(msg_type),repr(msg_version)))
            logging.debug("Processing message of type {}:{}".format(msg_type, msg_version))
            obj = models.FirePixel()
            obj = self.translators[msg_type][msg_version](data, obj)
            obj.save()
            logging.debug("Succesfully stored FirePixel record in the database".format(msg_type, msg_version))
        except Exception, e:
            logging.exception(str(e))
            raise e


import time
import signal



def async_run_forever():
    logging.info("Setting up AMQP exchanges, consumers, producers...")

    '''try:    not implementing the internet based message queue for MESA
        consuming_exchange = ConsumingExchange(settings.MESA_FT_AMQP_EXCHANGE, conn=settings.MESA_FT_AMQP_URI)
        consuming_exchange.declare()
        consuming_exchange.bind_queue(queue='af_modis', exchange=settings.CSIR_AMQP_EXCHANGE, conn=settings.CSIR_AMQP_URI, routing_keys=['af_modis.#'])
    except Exception, e:
        logging.exception(e)
        logging.warn('Failed to bind to CSIR exchange.')
    '''

    fire_pixel_persistance = FirePixelPersistConsumer('firepixel')
    fire_pixel_persistance.declare()
    fire_pixel_persistance.purge()
    fire_pixel_persistance.bind_queue(routing_keys=['af_modis.#'])
    fire_pixel_persistance.bind_queue(routing_keys=['af_viirs.#'])
    

    logging.info("AMQP running forever!")
    async.run_forever()
