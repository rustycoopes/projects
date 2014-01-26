import logging

from sonos_jukebox_config.models import ConfigManager
from sonos_jukebox_config.models import JukeboxShortCutManager
from sonos_pandora.sonos_pandora import SonosForPandora
from sonos_hardware.statuslcd import LCDScreen
from time import sleep

# ----------------------------------------------------------------------------------------
# Class purpose
#    Looks after the co-ordination betweek getting a key press and then telling the music
#    System what to do with it
# ----------------------------------------------------------------------------------------
class JukeboxKeyProcessor(object):
    
    # Gets the config mapping for a short cut, from its string value (i.e. value and type of track).
    shortCutMgr = None
    # Gets system config e.g. what speaker to play on
    configMgr = None
    # Interface into sonos.
    sonosPlayer = None
    
    def __init__(self):
        self.shortCutMgr = JukeboxShortCutManager()
        self.configMgr = ConfigManager()
        self.sonosPlayer = SonosForPandora()
        
    # ----------------------------------------------------------------------------------------
    # Process a key press, get the track and play it on the sonos box
    # ----------------------------------------------------------------------------------------
    def ProcessKey(self, shortCutKeys):
        logging.info('Sent short cut "%s"' % shortCutKeys)

        LCDScreen.updateStatus("Keys Received", shortCutKeys)

        try:
            shortCut = self.shortCutMgr.getShortCut(shortCutKeys)
        except:
            shortCut = None
            
        # Is this a known shortcut?
        if shortCut != None:
            
            LCDScreen.updateStatus("Shortcut", shortCut.track )
            speakerConfig = self.configMgr.getConifgItem( "TARGET_SPEAKER")
            
            logging.info('Short cut track is"%s" running from "%s"' % (shortCut.track, shortCut.type))
            logging.info('Successfully read speaker to send to as "%s"' % (speakerConfig.value))
            
            # tell sonos how to play its shortcut
            if shortCut.type =="Pandora":
                
                self.sonosPlayer = SonosForPandora()
                self.sonosPlayer.playStation(shortCut.track, speakerConfig.value)
            
            else:
                logging.error('Unsupported shortcut type %s' % shortCut.type )
                LCDScreen.updateStatus("ERROR", "UNK: %s" % shortCut.type )
                sleep(5)
            
            LCDScreen.updateStatus("Sonos Jukebox", "Ready....")
        
        else:
            logging.error('Shortcut not found for %s' % shortCutKeys )
            LCDScreen.updateStatus("ERROR", "UNK: %s" % shortCutKeys )
            sleep(5)

