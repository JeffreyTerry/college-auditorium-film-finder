# -*- coding: utf-8 -*-
from django.db import models
from jsonfield import JSONField
from datetime import datetime
import pytz
import re
import logging

logger = logging.getLogger(__name__)

# There should only ever be one Dankswank object
class Dankswank(models.Model):
    last_update = models.DateTimeField()

    @staticmethod
    def get_last_update():
        dankswank = Dankswank.objects.all()
        if dankswank:
            return dankswank[0].last_update
        else:
            return "never"

    @staticmethod
    def set_last_update():
        dankswank = Dankswank.objects.all()
        now = datetime.utcnow().replace(tzinfo=pytz.utc)
        if dankswank:
            dankswank[0].last_update = now
            dankswank[0].save()
        else:
            Dankswank(last_update=now).save()
