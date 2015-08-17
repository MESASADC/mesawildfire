# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AfModis',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(default=b'', max_length=40, blank=True)),
                ('point', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('lon', models.FloatField()),
                ('lat', models.FloatField()),
                ('date_time', models.DateTimeField(null=True, blank=True)),
                ('src', models.CharField(default=b'', max_length=20, blank=True)),
                ('sat', models.CharField(default=b'', max_length=20, blank=True)),
                ('frp', models.DecimalField(max_digits=4, decimal_places=2)),
                ('btemp', models.DecimalField(max_digits=4, decimal_places=2)),
            ],
        ),
    ]
