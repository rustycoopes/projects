'''
Created on Oct 19, 2013

@author: rusty
'''
import logging

from sonos_jukebox_config.models import ConfigManager
from sonos_jukebox_config.models import JukeboxShortCutManager
from sonos_pandora.sonos_pandora import SonosForPandora
from sonos_hardware.statuslights import ProgramStatusManager
from sonos_hardware.statuslights import ProgramStatus



class JukeboxKeyProcessor(object):
    
    statusManager = None
    shortCutMgr = None
    configMgr = None
    sonosPlayer = None
    
    def __init__(self):
        self.statusManager = ProgramStatusManager()
        self.statusManager.start()
        self.shortCutMgr = JukeboxShortCutManager()
        self.configMgr = ConfigManager()
        self.sonosPlayer = SonosForPandora()
        ProgramStatusManager.updateStatus(ProgramStatus.Waiting)
    
    def ProcessKey(self, shortCutKeys):
        
        
        logging.info('Sent short cut "%s"' % shortCutKeys)
        ProgramStatusManager.updateStatus(ProgramStatus.ReceivedKeys)
        shortCut = self.shortCutMgr.getShortCut(shortCutKeys)
        
        if shortCut != None:
            
            speakerConfig = self.configMgr.getConifgItem( "TARGET_SPEAKER")
            
            logging.info('Short cut track is"%s" running from "%s"' % (shortCut.track, shortCut.type))
            logging.info('Successfully read speaker to send to as "%s"' % (speakerConfig.value))
            
            if shortCut.type =="Pandora":
                
                self.sonosPlayer = SonosForPandora()
                self.sonosPlayer.playStation(shortCut.track, speakerConfig.value)
            
            else:
                logging.error('Unsupported shortcut type %s' % shortCut.type )
            
            ProgramStatusManager.updateStatus(ProgramStatus.Waiting)
        
        else:
            logging.error('Shortcut not found for %s' % shortCutKeys )
