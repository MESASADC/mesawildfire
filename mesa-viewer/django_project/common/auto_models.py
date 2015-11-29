# This file is generated automatically from the database by running ../update_common_models.sh.
# Do not manually edit this file because any changes will be lost when a new file is generated.
# The models can be customized by editing models.py in this directory.

from django.contrib.auth.models import User as AuthUser

# This is an auto-generated Django model module.

from django.db import models

class Organisation(models.Model):
    organisation_name = models.CharField(max_length=256)
    priority_messaging = models.BooleanField()
    class Meta:
        db_table = 'organisation'

# This is an auto-generated Django model module.

from django.db import models

class UserProfile(models.Model):
    user = models.ForeignKey(AuthUser)
    organisation = models.ForeignKey(Organisation)
    timezone = models.CharField(max_length=256)
    class Meta:
        db_table = 'user_profile'

