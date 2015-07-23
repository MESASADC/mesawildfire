#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys, os
import logging
from kombu import Connection, Exchange, Queue
import datetime

"""
with Connection('amqp://vhost1:password1@localhost:5672/vhost1/') as conn:
    simple_queue = conn.SimpleQueue('mesa_af_modis')
    message = 'helloword, sent at %s' % datetime.datetime.today()
    simple_queue.put(message)
    print('Sent: %s' % message)
    simple_queue.close()
"""


with Connection('amqp://vhost1:password1@localhost:5672/vhost1') as conn:
    conn.connect()
    print "conn"
    news_exchange = Exchange('news', type='topic', channel=conn.default_channel)
    news_exchange.declare()
    print "exchange"
    queue = Queue('news_queue', channel=conn.default_channel)
    queue.declare()
    print "queue"
    for n in range(60):
        queue.bind_to(exchange=news_exchange, routing_key='news.%d' % n)
        print "bound %d" % n
    queue.consume()
    print "consumed"
    conn.close()
    print "closed"
    
    
    
