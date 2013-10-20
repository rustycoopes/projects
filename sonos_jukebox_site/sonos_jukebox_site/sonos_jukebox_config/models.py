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

class ConfigManager(object):
    
    def getConifgItem(self, name):
        return Configuration.objects.get(key=name)

class JukeboxShortCutManager(object):
    
    def getShortCut(self, name):
        return JukeboxShortCut.objects.get(keys=name)




class JukeboxShortCut(models.Model):
    PANDORA = 'Pandora'
    TRACK_TYPE = (
        (PANDORA, 'Pandora'),
    )
    
    keys = models.CharField(max_length=3)
    type = models.CharField(max_length=255, choices=TRACK_TYPE, default=PANDORA)
    track = models.CharField(max_length=255)

 
    def __unicode__(self):
        return self.keys
    
    
