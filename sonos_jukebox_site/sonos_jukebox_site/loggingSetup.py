'''
Created on Oct 15, 2013

@author: rusty
'''
import logging

class LoggingInitialisation(object):
    '''
    classdocs
    '''
    def setupLogging(self):
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%m-%d %H:%M', filename='sonos-jukebox-server.log', filemode='w')
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)    
        # set a format which is simpler for console use
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        # tell the handler to use this format
        console.setFormatter(formatter)
        # add the handler to the root logger
        logging.getLogger('').addHandler(console)    
