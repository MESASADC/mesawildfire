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


#fire_status_choices = (('hotspot', 'Hotspot'), ('merged', 'Merged'), ('confirmed', 'Confirmed'), ('out', 'Out'))
fire_status_choices = {'hotspot': 'Hotspot', 'merged': 'Merged', 'confirmed': 'Confirmed', 'out': 'Out'}


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

    type_choices = (('int', 'Integer'), ('float', 'Float'), ('str', 'String'))
    
    name = models.CharField(max_length=50, blank=False, primary_key=True)
    type = models.CharField(max_length=20, blank=False, choices=type_choices, default='str')
    value = models.CharField(max_length=100, blank=True, null=True)


class FireCluster(models.Model, NotifySave):

    description = models.CharField(max_length=100, blank=True, default='')
    status = models.CharField(max_length=20, blank=True, choices=fire_status_choices.items(), default='')
    border = models.PolygonField()

    def __str__(self):
        return '{0} ({1})'.format(self.description, fire_status_choices.get(self.status, '_'))

        

class FirePixel(models.Model, NotifySave):

    type = models.CharField(max_length=40, blank=True, default='')
    point = models.PointField()
    vsize = models.FloatField(blank=False, default=0) 
    hsize = models.FloatField(blank=False, default=0) 
    date_time = models.DateTimeField(blank=True, null=True)
    src = models.CharField(max_length=20, blank=True, null=False, default='')
    sat = models.CharField(max_length=20, blank=True, null=False, default='')
    frp = models.FloatField(blank=True, null=True)
    btemp = models.FloatField(blank=True, null=True)
    to_cluster = models.BooleanField(blank=False, default=False)

    fire = models.ForeignKey(FireCluster, blank=True, null=True)
    
    @property
    def lat(self):
        return point.y

    @property
    def lon(self):
        return point.x

class FireEvent(View, NotifySave):

    description = models.CharField(max_length=50, blank=True, default='')
    status = models.CharField(max_length=20, blank=True, choices=fire_status_choices.items(), default='')

    border = models.PolygonField()
    area = models.FloatField()
    first_seen = models.DateTimeField()
    last_seen = models.DateTimeField()
    max_frp = models.FloatField()
    max_frp_date = models.DateTimeField()
    current_fdi = models.IntegerField()
    current_fdi_date = models.DateTimeField()
    start_fdi = models.IntegerField()
    max_fdi = models.IntegerField()
    max_fdi_date = models.DateTimeField()

    west = models.FloatField()
    east = models.FloatField()
    south = models.FloatField()
    north = models.FloatField()
    centroid_x = models.FloatField()
    centroid_y = models.FloatField()

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
    
    fdi_point = models.ForeignKey(FdiPoint)

class FdiGraphData(View):
    """ 
    A Django model that provides read-only access to a database view that provides 
    Fdi Graph data based on a join between FdiPoints and FdiMeasurements and FdiForecasts. 
    """
    point_id = models.IntegerField()
    point_name = models.CharField(max_length=100)

    value = models.FloatField()
    value_class = models.CharField(max_length=20)
    target_date_time = models.DateTimeField()

def _notification(event, instance):
    
    messages = []

    # update the model instance from the database to reflect changes made by database triggers (firepixel clustering happens in the database)
    instance = type(instance).objects.get(pk=instance.pk)

    message = {
              "pk": instance.pk,
              "rk": "notify.db.%s.%s" % (type(instance).__name__, event),
              "version": "0.1",
              "source": type(instance).__name__,
              "event": event,
              "timestamp": timezone.now().isoformat(),
              "extra" : { "fire_id" : instance.fire_id }
        }

    messages.append(message)
    

    if isinstance(instance, FirePixel):
        logging.debug('Event (%s) is for instance of FirePixel' % event)

        try:
            fire_event = FireEvent.objects.get(pk=instance.fire_id)
        except FireEvent.DoesNotExist, e:
            logging.debug('No fireEvent exists with pk=%s' % instance.fire_id)
            fire_event = None
        
        if fire_event:
            message = {
                  "pk": fire_event.pk,
                  "rk": "notify.db.FireEvent.cascaded",
                  "version": "0.1",
                  "source": type(instance).__name__,
                  "event": event,
                  "timestamp": timezone.now().isoformat(),
                  "extra": { "fire_pixel": instance.pk }
            }
            
            messages.append(message)

    return messages

@receiver(post_save, dispatch_uid='post_save_notify')
def post_save_notify_amqp(sender, **kwargs):
    logging.debug('post_save_notify_amqp: %s' % sender.__name__)
    instance = kwargs.get('instance')
    if issubclass(sender, NotifySave):
        event = 'created' if kwargs.get('created', False) else 'updated'
        logging.debug('post_save_notify_amqp: %s %s' % (sender.__name__, event))
        logging.info('Acquiring connection: %s' % settings.MESA_FT_AMQP_URI)
        try:
            with connections[Connection(settings.MESA_FT_AMQP_URI)].acquire(block=True) as conn:
                logging.info('Got connection. Acquiring producer...')
                with producers[conn].acquire(block=True, timeout=10) as producer:
                    logging.info('Got producer. Publishing to: %s' % settings.MESA_FT_AMQP_URI)
                    messages = _notification(event, instance)
                    for message in messages:
                        logging.debug(message)
                        rk = message.get('rk')
                        if not rk:
                            raise KeyError('Notification message should contain "rk" key')
                        producer.publish(
                            message,
                            exchange=settings.MESA_FT_AMQP_EXCHANGE,
                            routing_key=rk,
                            serializer='json')
        except Exception, e:
            logging.warn('Failed to publish (post save). Reason: %s' % e)
            if False and settings.DEBUG is True:
                raise e
   
