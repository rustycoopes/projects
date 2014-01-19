'''
Created on Oct 19, 2013

@author: rusty
'''
import logging
import datetime
import threading
import sys
from time import sleep
from django.core.management.base import BaseCommand, CommandError
from sonos_jukebox_config.models import ConfigManager
from sonos_jukebox_config.models import JukeboxShortCutManager
from sonos_pandora.sonos_pandora import SonosForPandora
from sonos_hardware.jukeboxinput import JukeboxSignalReceiver
from sonos_hardware.jukeboxinput import JukeboxSignalCallback
from sonos_jukebox_config.splashscreen import SplashScreen
from sonos_jukebox_config.buttonpressprocessor import JukeboxKeyProcessor
from sonos_hardware.statuslcd import ProgramStatusScreenManager

class JukeboxService(JukeboxSignalCallback):

    signalReceiver = None
    keyProcessor = None
    currentKey = None
    currentKeyUpdateTime = None
    splash = None
    
    letterTrainCounter = 0
    numberTrainCounter = 0
    lastSignalTime = None
    
    MAX_INTRA_TRAIN_GAP = 1
    MAX_MID_TRAIN_GAP = 3
    MAX_RESTART_PRESS = 5
    SIGNAL_NOT_SET = 0
    
    signalLock = None
    
    def __init__(self):
        super(JukeboxService, self).__init__()
        try:
            self.splash = SplashScreen()
            self.signalReceiver = JukeboxSignalReceiver(self)
            self.keyProcessor = JukeboxKeyProcessor()
            self.signalReceiver.start()
            self.lastSignalTime = datetime.datetime.now()
            self.signalLock = threading.Lock()
        except:
            logging.error('Error initialising jukebox service %s' % sys.exc_info()[1])


    def Run(self):
        logging.info( 'Jukebox Service running')
        self.lastSignalTime = datetime.datetime.now()
        self.splash.ShowSplash()
        ProgramStatusScreenManager.updateStatus("Sonos Jukebox", "Ready....")
        
        while 1:
            sleep(.25)
            keyPress =  self.SignalsToKeyUpdater()

            if keyPress != None :
                logging.info( 'Key press waiting to be processed.  Sending to processor')
                self.keyProcessor.ProcessKey(keyPress)
                ProgramStatusScreenManager.updateStatus("Sonos Jukebox", "Ready....")


    def Signalled(self):
        logging.info( 'Received signal')
        
        timeSinceLastSignal = datetime.datetime.now() - self.lastSignalTime

        logging.info("Aquiring lock on train counters for incrementing")
        self.signalLock.acquire()
        
        if self.letterTrainCounter == self.SIGNAL_NOT_SET:
            logging.info("Start of new button press - starting the letter count")
            self.letterTrainCounter = 1
            self.numberTrainCounter = self.SIGNAL_NOT_SET
        elif timeSinceLastSignal.seconds >= self.MAX_INTRA_TRAIN_GAP and timeSinceLastSignal.seconds <= self.MAX_MID_TRAIN_GAP:
            logging.info(" 1-3 sec delay is starting number train")
            self.numberTrainCounter = 1
        elif timeSinceLastSignal.seconds < self.MAX_INTRA_TRAIN_GAP:
            if self.numberTrainCounter == self.SIGNAL_NOT_SET :
                self.letterTrainCounter = self.letterTrainCounter + 1
                logging.info("Incrementing letter train, now %s" % self.letterTrainCounter)
            else:
                self.numberTrainCounter = self.numberTrainCounter + 1
                logging.info("Incrementing number train, now %s" % self.numberTrainCounter)
        else:
            logging.info("Ignored press %s seconds since last" % timeSinceLastSignal.seconds)
        self.lastSignalTime = datetime.datetime.now()
        self.signalLock.release()

    def SignalsToKeyUpdater(self):
        
        timeSinceLastSignal = datetime.datetime.now() - self.lastSignalTime
        
        if timeSinceLastSignal.seconds > self.MAX_RESTART_PRESS and self.letterTrainCounter != self.SIGNAL_NOT_SET:
            logging.info("Aquiring lock on train counters for resetting TIMEOUT")
            self.signalLock.acquire()
            self.letterTrainCounter = self.SIGNAL_NOT_SET
            self.numberTrainCounter = self.SIGNAL_NOT_SET
            self.signalLock.release()
            return None
        
        elif self.letterTrainCounter != self.SIGNAL_NOT_SET and self.numberTrainCounter != self.SIGNAL_NOT_SET and timeSinceLastSignal.seconds > self.MAX_MID_TRAIN_GAP:
            logging.info("Signals ready to process")
        
            logging.info("Aquiring lock on train counters for resetting")
            self.signalLock.acquire()
            si = SignalInterpretor()
            currentKey = si.Interpret(self.letterTrainCounter, self.numberTrainCounter)
        
            self.letterTrainCounter = self.SIGNAL_NOT_SET
            self.numberTrainCounter = self.SIGNAL_NOT_SET
            self.signalLock.release()
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
        logging.info( 'Service command starting')
        svc = JukeboxService()
        svc.Run()
        logging.info( 'Service command ending')
     


