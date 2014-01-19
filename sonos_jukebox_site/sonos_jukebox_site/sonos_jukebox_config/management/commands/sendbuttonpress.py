'''
Created on Oct 19, 2013

@author: rusty
'''
import logging
import sys
from django.core.management.base import BaseCommand, CommandError
from sonos_jukebox_config.models import ConfigManager
from sonos_jukebox_config.models import JukeboxShortCutManager
from sonos_pandora.sonos_pandora import SonosForPandora
from sonos_hardware.statuslights import ProgramStatusManager
from sonos_hardware.statuslights import ProgramStatus
from sonos_jukebox_config.buttonpressprocessor import JukeboxKeyProcessor
from sonos_hardware.statuslcd import ProgramStatusScreenManager
from sonos_jukebox_config.splashscreen import SplashScreen
f


class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'


    def handle(self, *args, **options):
        try:
            splash = SplashScreen()
            splash.ShowSplash()
            keyProcessor = JukeboxKeyProcessor()
        
            for shortCutKeys in args:
                keyProcessor.ProcessKey(shortCutKeys)
        except:
            logging.error('Error processing press %s' % sys.exc_info()[1])
            

