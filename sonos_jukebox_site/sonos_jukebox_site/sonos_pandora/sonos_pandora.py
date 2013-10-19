import sys

from soco import SoCo
from soco import SonosDiscovery
from russpandora import RussPandora
import logging

class SonosForPandora(object):
    

    rpandora = None
    sonos = None

    def __init__(self):
        self.rpandora = RussPandora()
        self.sonos = SonosDiscovery()
        logging.info('found the following sonos servers : ' + ','.join(self.sonos.get_speaker_ips()))
 
    
    def playStation(self, stationNameLike, onSpeakerLike): 
  
        stationId = self.rpandora.getIdForStation(stationNameLike)
        
        for speakerIp in self.sonos.get_speaker_ips():
            all_info = sonos.get_speaker_info()
            if onSpeakerLike in all_info['zone_name'] :
                logging.info("Playing on speaker %s" % str(speakerIp))
                sonos = SoCo(str(speakerIp))
                sonos.play_uri("pndrradio:%s" % str(stationId), '')
                     
    def stopPlaying(self):
        
        for speakerIp in self.sonos.get_speaker_ips():
            sonos = SoCo(speakerIp)
            all_info = sonos.get_speaker_info()
            for item in all_info:
                logging.info("Stopping for speaker %s: %s" % (item, all_info[item]))
            sonos.stop()


    def listAll(self):
    
        for speakerIp in self.sonos.get_speaker_ips():
            logging.info("********* %s ***********" % str(speakerIp))
            sonos = SoCo(speakerIp)
            all_info = sonos.get_speaker_info()
            for item in all_info:
                logging.info("    %s: %s" % (item, all_info[item]))
            logging.info('co-ordinator = ' + str(sonos.get_group_coordinator(all_info['zone_name'], True)))
            logging.info("****************************" )
           

if __name__ == "__main__":
  
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%m-%d %H:%M', filename='sonos-jukebox-server.log', filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)    
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)    
    
    
    sonos = SonosForPandora()
    sonos.listAll()
    sonos.playStation('Rod', 'Kitchen')    