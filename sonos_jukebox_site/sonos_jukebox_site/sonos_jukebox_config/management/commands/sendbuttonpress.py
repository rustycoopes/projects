'''
Created on Oct 19, 2013

@author: rusty
'''
import logging
from django.core.management.base import BaseCommand, CommandError
from sonos_jukebox_config.models import ConfigManager
from sonos_jukebox_config.models import JukeboxShortCutManager
from sonos_pandora.sonos_pandora import SonosForPandora

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        shortCutMgr = JukeboxShortCutManager()
        
     
        mgr = ConfigManager()
        for shortCutKeys in args:
            
            logging.info('Sent short cut "%s"' % shortCutKeys)
            shortCut = shortCutMgr.getShortCut(shortCutKeys)
            
            if shortCut != None:
            
                speakerConfig = mgr.getConifgItem( "TARGET_SPEAKER")
                logging.info('Short cut track is"%s" running from "%s"' % (shortCut.track, shortCut.type))
                logging.info('Successfully read speaker to send to as "%s"' % (speakerConfig.value))
                
                if shortCut.type =="Pandora":
                    sonosPlayer = SonosForPandora()
                    sonosPlayer.playStation(shortCut.track, speakerConfig.value)
                else:
                    logging.error('Unsupported shortcut type %s' % shortCut.type )   
            else:
                logging.error('Shortcut not found for %s' % shortCutKeys )   