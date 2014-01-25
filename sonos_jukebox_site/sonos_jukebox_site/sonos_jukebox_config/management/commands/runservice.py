
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
from sonos_hardware.statuslcd import LCDScreen



# ----------------------------------------------------------------------
# Class Purpose
#   Main application entry point.  This listens to the Jukebox the jukebox
#   electrical signals as a set of on/offs..  this calculates the number of
#   them and the seperation between letter and number.  This is then passed
#   on as a shortcut to process
# ----------------------------------------------------------------------
class JukeboxService(JukeboxSignalCallback):

    signalReceiver = None
    keyProcessor = None
    currentKey = None
    currentKeyUpdateTime = None
    
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
            self.signalReceiver = JukeboxSignalReceiver(self)
            self.keyProcessor = JukeboxKeyProcessor()
            self.signalReceiver.start()
            self.lastSignalTime = datetime.datetime.now()
            self.signalLock = threading.Lock()
        except:
            logging.error('Error initialising jukebox service %s' % sys.exc_info()[1])

    #----------------------------------------------------------------------------
    # Listens to hear key presses, then updates processes them if we have any
    #----------------------------------------------------------------------------
    def Run(self):
        logging.info( 'Jukebox Service running')
        self.lastSignalTime = datetime.datetime.now()
        LCDScreen.updateStatus("Sonos Jukebox", "Ready....")
        
        while 1:
            # get any key presses
            keyPress =  self.SignalsToKeyUpdater()

            # if there are any, then process them !
            if keyPress != None :
                logging.info( 'Key press waiting to be processed.  Sending to processor')
                self.keyProcessor.ProcessKey(keyPress)
                LCDScreen.updateStatus("Sonos Jukebox", "Ready....")
 
    #----------------------------------------------------------------------------
    # Call back method from hardware monitor.  This gets the call backs and then
    # Tries to read them as a number of letter counts and number counts..
    # This works out the train start and end.  This update will happen on another thread
    #----------------------------------------------------------------------------
    def Signalled(self):
        logging.info( 'Received signal')
        
        timeSinceLastSignal = datetime.datetime.now() - self.lastSignalTime

        logging.info("Aquiring lock on train counters for incrementing")
        self.signalLock.acquire()
        
        # No previous signal, we are just starting to get one.
        if self.letterTrainCounter == self.SIGNAL_NOT_SET:
            logging.info("Start of new button press - starting the letter count")
            self.letterTrainCounter = 1
            self.numberTrainCounter = self.SIGNAL_NOT_SET
            
        # there has been a pause and we have restarted getting signals. this will be the gap between numbers and letters.
        elif timeSinceLastSignal.seconds >= self.MAX_INTRA_TRAIN_GAP and timeSinceLastSignal.seconds <= self.MAX_MID_TRAIN_GAP:
            logging.info(" 1-3 sec delay is starting number train")
            self.numberTrainCounter = 1
        
        # timeout.. either we have read everything or not - nothing else if happening.
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

    
    #----------------------------------------------------------------------------
    #try to read the letter and number count...
    # Compexity is that the counts are updated on another thread.  We need to see if
    # We have left sufficient time for all information to be in.  If we do, read it
    # Then reset the data.
    #----------------------------------------------------------------------------
    def SignalsToKeyUpdater(self):
        
        timeSinceLastSignal = datetime.datetime.now() - self.lastSignalTime
        
        # Read timed out we have numbers but no letters- ignore data.
        if timeSinceLastSignal.seconds > self.MAX_RESTART_PRESS and self.letterTrainCounter != self.SIGNAL_NOT_SET:
            logging.info("Aquiring lock on train counters for resetting TIMEOUT")
            self.signalLock.acquire()
            self.letterTrainCounter = self.SIGNAL_NOT_SET
            self.numberTrainCounter = self.SIGNAL_NOT_SET
            self.signalLock.release()
            return None
        
        # Data is ready to return. - we have letter and number counts, and we have left enough time to ensure there are no more ocming.
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


# ----------------------------------------------------------------------
# Class Purpose
#   Povie a mapping between signal peaks and the actual Key value e.g.
#   110100111  = A1
#   taken is as a number of letter blips and a count of number blips
# ----------------------------------------------------------------------
class SignalInterpretor(object):

    def Interpret(self, letterTrainCounter, numberTrainCounter):
        letterDict = dict({1:"A", 2:"B"})
        return "%s%s" % (letterDict[letterTrainCounter], numberTrainCounter)



# ----------------------------------------------------------------------
# Class Purpose
#   Django entry point for this service
# ----------------------------------------------------------------------
class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        try:
            splash = SplashScreen()
            splash.ShowSplash()
            logging.info( 'Service command starting')
            svc = JukeboxService()
            svc.Run()
            logging.info( 'Service command ending')
        except:
            logging.error('Error running service %s' % sys.exc_info()[1])
            LCDScreen.updateStatus("ERROR",  sys.exc_info()[1] )
     


