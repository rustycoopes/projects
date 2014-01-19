'''
Created on Oct 19, 2013

@author: rusty
'''
import logging

from sonos_jukebox_config.models import ConfigManager
from sonos_jukebox_config.models import JukeboxShortCutManager
from sonos_pandora.sonos_pandora import SonosForPandora
from sonos_hardware.statuslcd import ProgramStatusScreenManager
from time import sleep


class JukeboxKeyProcessor(object):
    
    shortCutMgr = None
    configMgr = None
    sonosPlayer = None
    
    def __init__(self):
        self.shortCutMgr = JukeboxShortCutManager()
        self.configMgr = ConfigManager()
        self.sonosPlayer = SonosForPandora()
   
    def ProcessKey(self, shortCutKeys):
        logging.info('Sent short cut "%s"' % shortCutKeys)

        ProgramStatusScreenManager.updateStatus("Keys Received", shortCutKeys)

        shortCut = self.shortCutMgr.getShortCut(shortCutKeys)
        
        ProgramStatusScreenManager.updateStatus("Shortcut", shortCut.track )
        if shortCut != None:
            
            speakerConfig = self.configMgr.getConifgItem( "TARGET_SPEAKER")
            
            logging.info('Short cut track is"%s" running from "%s"' % (shortCut.track, shortCut.type))
            logging.info('Successfully read speaker to send to as "%s"' % (speakerConfig.value))
            
            if shortCut.type =="Pandora":
                
                self.sonosPlayer = SonosForPandora()
                self.sonosPlayer.playStation(shortCut.track, speakerConfig.value)
            
            else:
                logging.error('Unsupported shortcut type %s' % shortCut.type )
                ProgramStatusScreenManager.updateStatus("ERROR", "UNK:" % shortCut.type )
                sleep(5)
            
            ProgramStatusScreenManager.updateStatus("Sonos Jukebox", "Ready....")
        
        else:
            logging.error('Shortcut not found for %s' % shortCutKeys )
            ProgramStatusScreenManager.updateStatus("ERROR", "UNK:" % shortCutKeys )
            sleep(5)

