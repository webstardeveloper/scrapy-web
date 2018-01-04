from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext as _
# Create your models here.

class License(models.Model):
    license_number = models.CharField(_('license_number'), max_length=100, null=True)
    name = models.CharField(_('name'), max_length=255, null=True)
    license_type = models.CharField(_('license_type'), max_length=255, null=True)
    primary_status = models.CharField(_('primary_status'), max_length=255, null=True)
    previous_names = models.CharField(_('previous_names'), max_length=255, null=True)
    address = models.CharField(_('address'), max_length=255, null=True)
    issuance_date = models.CharField(_('issuance_date'), max_length=100, null=True)
    expiration_date = models.CharField(_('expiration_date'), max_length=100, null=True)
    current_date_time = models.CharField(_('current_date_time'), max_length=100, null=True)
    source_url = models.CharField(_('source_url'), max_length=255, null=True)

    def __unicode__(self):
        return self.license_number