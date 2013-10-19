'''
Created on Oct 13, 2013
python manage.py syncdb
python manage.py runserver
@author: russcooper
'''

from django.db import models

class Configuration(models.Model):
    key = models.CharField(max_length=70)
    value = models.CharField(max_length=255)

    def __unicode__(self):
        return self.key


class JukeboxShortCut(models.Model):
    keys = models.CharField(max_length=3)
    type = models.CharField(max_length=255)
    track = models.CharField(max_length=255)

    def __init__(self):
        self.type = 'Pandora'
 
    def __unicode__(self):
        return self.keys

