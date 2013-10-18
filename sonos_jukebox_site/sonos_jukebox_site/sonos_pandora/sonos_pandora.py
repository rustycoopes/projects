import sys

from soco import SoCo
from soco import SonosDiscovery
from russpandora import RussPandora
import logging

class SonosForPandora(object):
    '''
    classdocs
    '''
    rpandora = None
    sonos = None

    def __init__(self):
        sonos = SonosDiscovery()
        logging.info('found the following sonos servers : ' + ','.join(sonos.get_speaker_ips()))
 
    
    def playStation(self, stationNameLike): 
        if self.rpandora is None:
            self.rpandora = RussPandora()
        if self.sonos is None:
            self.sonos = SonosDiscovery()    
        
        stationId = self.rpandora.getIdForStation(stationNameLike)
        
        masterId =  self.sonos.get_speaker_ips()[0]
        
        for speakerIp in self.sonos.get_speaker_ips():
            logging.info(str(speakerIp))
            sonos = SoCo(str(speakerIp))
            all_info = sonos.get_speaker_info()
            for item in all_info:
                logging.info("    %s: %s" % (item, all_info[item]))
            logging.info('co-ordinator = ' + str(sonos.get_group_coordinator(all_info['zone_name'], True)))
            if sonos.get_group_coordinator(all_info['zone_name'], True) is not None:
                sonos.unjoin()

          
                        
                     
    def stopPlaying(self):
        
        for speakerIp in self.sonos.get_speaker_ips():
            sonos = SoCo(speakerIp)
            all_info = sonos.get_speaker_info()
            for item in all_info:
                logging.info("Stopping for speaker %s: %s" % (item, all_info[item]))
            sonos.stop()


if __name__ == "__main__":
  
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%m-%d %H:%M', filename='sonos-jukebox-server.log', filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)    
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)    
    
    
    sonos = SonosForPandora()
    sonos.playStation('Rod')
    