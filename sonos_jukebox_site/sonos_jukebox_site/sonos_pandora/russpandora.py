'''
Created on Oct 15, 2013

@author: rusty
'''
from pandora import Pandora
import logging


class RussPandora(object):

    stationList = None
    
    def __init__(self):
        '''
        Constructor
        '''
           
           
    def getIdForStation(self, stationNameLike):
        
        if self.stationList == None:
            logging.info( "logging into pandora")
            russPandora = Pandora()
            username = "russell.cooper@btinternet.com"
            password = "cooperman"
            russPandora.authenticate(username, password)
            logging.info(  "loading station list")
            self.stationList = russPandora.get_station_list()
            logging.info(  "station list loaded ")
        
        stationId = -1
        for station in self.stationList:
            if stationNameLike in station['stationName']:
                stationId = station['stationId']
                logging.info( 'found track "%s"' % station['stationName'])
                return stationId
            
        
        logging.error(  'error no station found')
        return -1
        
        
       
if __name__ == "__main__":
  
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%m-%d %H:%M', filename='sonos-jukebox-server.log', filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)    
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)    
    rp = RussPandora()
    print 'station id for Phil is ' + str(rp.getIdForStation('Phil'))
    print 'station id for Coming is ' + str(rp.getIdForStation('Coming'))
    print 'station id for home is ' + str(rp.getIdForStation('home'))
    print 'station id for Home is ' + str(rp.getIdForStation('Home'))
    print 'station id for Queen is ' + str(rp.getIdForStation('Phil'))
    print 'station id for xyz is ' + str(rp.getIdForStation('xyz'))
