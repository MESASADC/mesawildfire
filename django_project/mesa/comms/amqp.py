#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys, os
import logging
import kombu
from kombu import Connection, Exchange, Queue
from kombu.async import Hub
import datetime
from functools import partial

from django.conf import settings


async = Hub()
    
logging.basicConfig(filename='/dev/stdout', format='%(levelname)s:    %(message)s', level=logging.DEBUG)


class Funnel(Exchange):
    
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
            
        super(Funnel, self).__init__(name=self.name, type=self.type, conn=self._conn, channel=self._channel, **kwargs)

        
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
        
        channel = channel or self._channel
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
        
        logging.info("Binding queue '%s' to exchange '%s' with:" % (queue.name, self.name))
        routing_keys = routing_keys or ['#']
        for rk in routing_keys:
            queue.bind_to(exchange=exchange, routing_key=rk)
            logging.debug("rk: %s" % rk)
            
        consumer_tag = '%s::%s::funnel' % (self.name, queue.name)
        queue.consume(consumer_tag, callback=self._consumer_producer_callback)
        
        self._queues.append(queue)
        return queue
        
    def _consumer_producer_callback(self, message):
        
        routing_key = message.delivery_info.get('routing_key')
        self.publish(message, routing_key)
        logging.info("published a message with rk '%s' to '%s'" % (routing_key, self.name))
        message.ack()

def async_run_forever():
    logging.info("Setting up AMQP exchanges, consumers, producers...")
    
    funnel = Funnel(settings.NOTIFY_SAVE_AMQP_EXCHANGE, conn=settings.NOTIFY_SAVE_AMQP_CONN_URI)
    funnel.declare()
    
    funnel.bind_queue('queue_1', settings.NOTIFY_SAVE_AMQP_EXCHANGE, routing_keys=['rk_a', 'rk_b'])
    funnel.bind_queue('queue_2', settings.NOTIFY_SAVE_AMQP_EXCHANGE, routing_keys=['rk_a', 'rk.2.a'])

    logging.info("AMQP running forever!")
    async.run_forever()

       
        
        
