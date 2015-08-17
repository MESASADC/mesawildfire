from django.contrib.gis.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.conf import settings

from kombu import Connection, Exchange
from kombu.pools import connections, producers

class NotifySave(object):
    pass


class AfModis(models.Model, NotifySave):

    type = models.CharField(max_length=40, blank=True, default='')
    point = models.PointField()
    lon = models.FloatField()
    lat = models.FloatField()
    date_time = models.DateTimeField(blank=True, null=True)
    src = models.CharField(max_length=20, blank=True, default='')
    sat = models.CharField(max_length=20, blank=True, default='')
    frp = models.FloatField()
    btemp = models.FloatField()




def _notification(event, source):
    return {
            "type": "notify",
            "version": "m.0.1",
            "event": event,
            "source": source,
        }



@receiver(post_save, dispatch_uid='post_save_notify')
def post_save_notify_amqp(sender, **kwargs):
    if isinstance(sender, NotifySave):
        event = 'created' if kwargs.get('created', False) else 'updated'
        with connections[Connection(settings.get('NOTIFY_SAVE_AMQP_CONN_URI'))].acquire(block=True, timeout=10) as conn:
            with producers[conn].acquire(block=True, timeout=10) as producer:
                producer.publish(
                    _notification(event, sender.__name__),
                    exchange=settings.get('NOTIFY_SAVE_AMQP_EXCHANGE', 'NOTIFY_SAVE_AMQP_EXCHANGE'),
                    routing_key='notify.save.%s.%s' % (sender.__name__, event),
                    serializer='json')
                
            
        
        
        
        
        
        
        
        
    
