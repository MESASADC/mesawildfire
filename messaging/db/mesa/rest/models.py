from django.contrib.gis.db import models


class AfModis(models.Model):
    type = models.CharField(max_length=40, blank=True, default='')
    point = models.PointField()
    lon = models.FloatField()
    lat = models.FloatField()
    date_time = models.DateTimeField(blank=True, null=True)
    src = models.CharField(max_length=20, blank=True, default='')
    sat = models.CharField(max_length=20, blank=True, default='')
    frp = models.DecimalField(decimal_places=2, max_digits=4)
    btemp = models.DecimalField(decimal_places=2, max_digits=4)
    
    

