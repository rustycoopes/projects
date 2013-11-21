'''
Created on Oct 19, 2013

@author: rusty
'''
import logging
from django.core.management.base import BaseCommand, CommandError
from sonos_jukebox_config.models import ConfigManager
from sonos_jukebox_config.models import JukeboxShortCutManager
from sonos_pandora.sonos_pandora import SonosForPandora
from sonos_hardware.statuslights import ProgramStatusManager
from sonos_hardware.statuslights import ProgramStatus

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'


    def handle(self, *args, **options):
        try:
            handleUnWrapped(self, args, options)
        except:
            logging.error('Error processing press %s' % , sys.exc_info()[0])
            

    def handleUnWrapped(self, *args, **options):
        
        shortCutMgr = JukeboxShortCutManager()
        configMgr = ConfigManager()
        statusManager = ProgramStatusManager()
        statusManager.start()
        ProgramStatusManager.updateStatus(ProgramStatus.Waiting)
        for shortCutKeys in args:
            
            logging.info('Sent short cut "%s"' % shortCutKeys)
            ProgramStatusManager.updateStatus(ProgramStatus.ReceivedKeys)
            shortCut = shortCutMgr.getShortCut(shortCutKeys)
            
            if shortCut != None:
            
                speakerConfig = configMgr.getConifgItem( "TARGET_SPEAKER")
                
                logging.info('Short cut track is"%s" running from "%s"' % (shortCut.track, shortCut.type))
                logging.info('Successfully read speaker to send to as "%s"' % (speakerConfig.value))
                
                if shortCut.type =="Pandora":
                    
                    sonosPlayer = SonosForPandora()
                    sonosPlayer.playStation(shortCut.track, speakerConfig.value)
                
                else:
                    logging.error('Unsupported shortcut type %s' % shortCut.type )   

                ProgramStatusManager.updateStatus(ProgramStatus.Waiting)
                            
            else:
                logging.error('Shortcut not found for %s' % shortCutKeys )   