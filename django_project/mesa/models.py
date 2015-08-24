from django.contrib.gis.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from django.conf import settings

from kombu import Connection, Exchange
from kombu.pools import connections, producers

import logging
logfile='/dev/stdout'
logging.basicConfig(filename=logfile,level=logging.DEBUG, format='[%(levelname)s] %(message)s')


class ViewManager(models.Manager):
    """ Django model manager class to enable read-only access to a database view"""

    def bulk_create(self, *args, **kwargs):
        raise NotImplementedError

    def create(self, *args, **kwargs):
        raise NotImplementedError

    def get_or_create(self, *args, **kwargs):
        raise NotImplementedError

    def delete(self, *args, **kwargs):
        raise NotImplementedError

    def update(self, *args, **kwargs):
        raise NotImplementedError


class View(models.Model):
    """ 
    Django model class to enable read-only access to a database view
    See:
        http://schinckel.net/2014/09/01/postgres-view-meet-django-model/
        https://gist.github.com/mattmcc/5250561
    """
    objects = ViewManager()

    class Meta:
        abstract = True
        managed = False

    def delete(self, *args, **kwargs):
        raise NotImplementedError

    def save(self, *args, **kwargs):
        raise NotImplementedError


class NotifySave(object):
    """ Class to add as parent to classes who should notify on save"""
    pass


class ConfigSetting(models.Model, NotifySave):

    notify = True
    type_choices = (('int', 'Integer'), ('float', 'Float'), ('str', 'String'))
    
    name = models.CharField(max_length=50, blank=False, primary_key=True)
    type = models.CharField(max_length=20, blank=False, choices=type_choices, default='str')
    value = models.CharField(max_length=100, blank=True, null=True)


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


class FdiPoint(models.Model, NotifySave):

    type_choices = (('wstation', 'Weather station'), ('poi', 'Point of interest'))
    
    name = models.CharField(max_length=40, blank=False, unique=True)
    type = models.CharField(max_length=20, blank=True, choices=type_choices, default='poi')
    point = models.PointField()
    lon = models.FloatField()
    lat = models.FloatField()

    station_name = models.CharField(max_length=40, blank=True, null=True, unique=True, default=None)
    station_id = models.CharField(max_length=40, blank=True, null=True, unique=True, default=None)

    def __str__(self):
        return '{0} ({1})'.format(self.name, self.type)

class FdiMeasurement(models.Model, NotifySave):

    rain_mm = models.FloatField()
    windspd_kmh = models.FloatField()
    winddir_deg = models.FloatField()
    rh_pct = models.FloatField()
    fdi_value = models.IntegerField()
    fdi_rgb = models.CharField(max_length=10, blank=True, null=False, default='')
    temp_c = models.FloatField()
    date_time = models.DateTimeField(blank=True, null=True)
    
    fdi_point = models.ForeignKey(FdiPoint, blank=True, null=True)


class FdiForecast(View):
    """ 
    A Django model that provides read-only access to a database view that provides 
    forecast values based on an intersection between FdiPoints and a PostGIS 2 raster table. 
    """
 
    rain_mm = models.FloatField()
    windspd_kmh = models.FloatField()
    winddir_deg = models.FloatField()
    rh_pct = models.FloatField()
    fdi_value = models.IntegerField()
    fdi_rgb = models.CharField(max_length=10, blank=True, null=False, default='')
    fwi_value = models.IntegerField()
    fwi_rgb = models.CharField(max_length=10, blank=True, null=False, default='')
    temp_c = models.FloatField()
    date_time = models.DateTimeField(blank=True, null=True)

    fdi_point = models.ForeignKey(FdiPoint, blank=True, null=True)


def _notification(event, source):
    return {
            "type": "notify.ui.db",
            "version": "m.0.1",
            "event": event,
            "source": source,
            "timestamp": timezone.now().isoformat()
        }


@receiver(post_save, dispatch_uid='post_save_notify')
def post_save_notify_amqp(sender, **kwargs):
    logging.debug('post_save_notify_amqp: %s' % sender.__name__)
    if sender.__dict__.get('notify', False):
        event = 'created' if kwargs.get('created', False) else 'updated'
        logging.debug('post_save_notify_amqp: %s %s' % (sender.__name__, event))
        logging.info('Acquiring connection: %s' % settings.NOTIFY_SAVE_AMQP_CONN_URI)
        with connections[Connection(settings.NOTIFY_SAVE_AMQP_CONN_URI)].acquire(block=True) as conn:
            logging.info('Got connection. Acquiring producer...')
            with producers[conn].acquire(block=True, timeout=10) as producer:
                logging.info('Got producer. Publishing to: %s' % settings.NOTIFY_SAVE_AMQP_EXCHANGE)
                producer.publish(
                    _notification(event, sender.__name__),
                    exchange=settings.NOTIFY_SAVE_AMQP_EXCHANGE,
                    routing_key='notify.ui.db.%s.%s' % (event, sender.__name__),
                    serializer='json')
                logging.info('Published.')
