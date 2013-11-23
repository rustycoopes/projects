'''
Created on Oct 19, 2013

@author: rusty
'''
import logging
import datetime
import threading
from time import sleep
from django.core.management.base import BaseCommand, CommandError
from sonos_jukebox_config.models import ConfigManager
from sonos_jukebox_config.models import JukeboxShortCutManager
from sonos_pandora.sonos_pandora import SonosForPandora
from sonos_hardware.jukeboxinput import JukeboxSignalManager
from sonos_hardware.jukeboxinput import JukeboxSignalCallback
from sonos_jukebox_config.buttonpressprocessor import JukeboxKeyProcessor

class JukeboxService(JukeboxSignalCallback):

    signalManager = None
    keyProcessor = None
    currentKey = None
    currentKeyUpdateTime = None
    
    letterTrainCounter = 0
    numberTrainCounter = 0
    lastSignalTime = None
    
    MAX_INTRA_TRAIN_GAP = 1
    MAX_MID_TRAIN_GAP = 3
    SIGNAL_NOT_SET = 0
    
    signalLock = None
    
    def __init__(self, jukeboxCallback):
        super(JukeboxSignalManager, self).__init__()
        try:
            self.signalManager = JukeboxSignalManager(self)
            self.keyProcessor = JukeboxKeyProcessor()
            self.signalManager.start()
            self.lastSignalTime = datetime.now()
        except:
            logging.error( 'GPIO Failed')


    def run(self):
        while 1:
            sleep(.25)
            keyPress =  self.SignalsToKeyUpdater()

            if keyPress != None :
                logging.info( 'Key press waiting to be processed.  Sending to processor')
                self.keyProcessor.Process(keyPress)


    def Signalled(self):
        logging.info( 'Received signal')
        
        timeSinceLastSignal = lastSignalTime - datetime.now()

        logging.info("Aquiring lock on train counters for incrementing")
        signalLock.aquire()
        
        if self.letterTrainCounter == SIGNAL_NOT_SET:
            logging.info("Start of new button press - starting the letter count")
            self.letterTrainCounter = 1
        elif timeSinceLastSignal.seconds >= MAX_INTRA_TRAIN_GAP and timeSinceLastSignal.seconds <= MAX_MID_TRAIN_GAP:
            logging.info(" 1-3 sec delay is starting number train")
            self.numberTrainCounter = 1
        elif timeSinceLastSignal.seconds < MAX_INTRA_TRAIN_GAP:
            if self.numberTrainCounter == SIGNAL_NOT_SET :
                logging.info("Incrementing letter train")
                self.letterTrainCounter = self.letterTrainCounter + 1
            elif
                logging.info("Incrementing number train")
                self.numberTrainCounter = self.numberTrainCounter + 1

        signalLock.release()

    def SignalsToKeyUpdater(self):
        
        if self.letterTrainCounter != SIGNAL_NOT_SET and self.numberTrainCounter != SIGNAL_NOT_SET and self.timeSinceLastSignal.seconds > MAX_MID_TRAIN_GAP:
            logging.info("Signals ready to process")
        
            logging.info("Aquiring lock on train counters for resetting")
            signalLock.aquire()
            si = SignalInterpretor()
            currentKey = si.Interpret(sel.letterTrainCounter, self.numberTrainCounter)
        
            self.letterTrainCounter = SIGNAL_NOT_SET
            self.numberTrainCounter = SIGNAL_NOT_SET
            signalLock.release()
            return currentKey
        else:
            return None

class SignalInterpretor(object):

    def Interpret(self, letterTrainCounter, numberTrainCounter):
        letterDict = dict({1:"A", 2:"B"})
        return "%s%s" % (letterDict[letterTrainCounter], numberTrainCounter)



class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        svc = JukeboxService()
        svc.Run()
     


