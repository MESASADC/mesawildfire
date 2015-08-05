from django.contrib.gis.db import models


class AfModis(models.Model):
    type = models.CharField(blank=True, default='')
    geom = models.PointField()
    lon = models.DecimalField()
    lat = models.DecimalField()
    date_time = models.DateTimeField()
    

