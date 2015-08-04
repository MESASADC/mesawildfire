#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys, os
import logging
import kombu
from kombu import Connection, Exchange, Queue
from kombu.async import Hub
import datetime
from functools import partial
from exceptions import NotImplementedError
import requests
import json


async = Hub()
    
logging.basicConfig(filename='/dev/stdout', format='%(levelname)s:    %(message)s', level=logging.DEBUG)

class Persist(Queue):
            
    def bind_queue(self, exchange, routing_keys=None, **kwargs):
            
        logging.info("Binding queue '%s' to exchange '%s' with:" % (self.name, exchange.name))
        routing_keys = routing_keys or ['#']
        for rk in routing_keys:
            queue.bind_to(exchange=exchange, routing_key=rk)
            logging.debug("rk: %s" % rk)
            
        consumer_tag = '%s::%s::persist' % (exchange.name, self.name)
        queue.consume(consumer_tag, callback=self._consumer_callback)

        return consumer_tag
        
    def _consumer_callback(self, message):
        
        routing_key = message.delivery_info.get('routing_key')
        
        self.publish(message, routing_key)
        logging.debug("%s is persisting a message with rk '%s'" % (self.name, routing_key))
        self._persist(message)
        message.ack()

    def _persist(self, message):
        raise NotImplementedError('Abstract persist method needs to be overridden')


class RestPost(Persist):
    
    def __init__(self, name, channel, uri, auth=None):
        
        super(RestPost, self).__init__(name, channel)
        
        self._uri = uri
        self._auth = auth
        
    def _persist(self, message, data):
        
        try:
            r = requests.post(self._uri, auth=self._auth, data=data)
            r.raise_for_status()
        except Exception, e:
            raise e
    
    
    

import time          
import signal


if __name__ == "__main__":
    
    rp = RestPost('restpost', channel=None, uri='http://www.afis.co.za')
    rp._persist(message='hallo', data={'key': 'value'})
    
    """
    uri = 'amqp://vhost1:password1@localhost:5672/vhost1'
    
    funnel = Funnel('my_funnel', conn=uri)
    funnel.declare()
    
    funnel.bind_queue('queue_1', 'my_funnel', routing_keys=['rk_a', 'rk_b'])
    funnel.bind_queue('queue_2', 'my_exchange', routing_keys=['rk_a', 'rk.2.a'])

    if False:  # throughput test

        def timeout(signum, frame):
            print 'signal'
            funnel.publish('A', 'rk_a')
            
        signal.signal(signal.SIGALRM, timeout)
        
        signal.setitimer(signal.ITIMER_REAL, 1, 0.5)

    async.run_forever()

    """
    
