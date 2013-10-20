'''
Created on Oct 19, 2013

@author: rusty
'''
import logging
from django.core.management.base import BaseCommand, CommandError
from sonos_jukebox_config.models import ConfigManager

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        
        mgr = ConfigManager()
        for poll_id in args:
            poll = mgr.getConifgItem( poll_id)
            logging.info('Successfully read config "%s"' % poll.value)