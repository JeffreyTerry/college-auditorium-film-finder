# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from jsonfield import JSONField
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
            return "Error: no updates available"

    @staticmethod
    def set_last_update():
        dankswank = Dankswank.objects.all()
        if dankswank:
            dankswank[0].last_update = timezone.now()
            dankswank[0].save()
        else:
            Dankswank(last_update=timezone.now()).save()
