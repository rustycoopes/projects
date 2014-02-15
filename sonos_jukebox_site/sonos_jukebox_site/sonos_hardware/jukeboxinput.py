import logging
import sys
import threading
import time
from breadboardinputs import BreadBoardInput
import RPi.GPIO as GPIO
from time import sleep

# ----------------------------------------------------------------------------------------
# Class Purpose
#   Provide a class that can continually check for a signal event on a background thread.
#   When an event is detected, then the call back is called 'Signalled'
#   THIS ONLY SIGNALS for ON events.  e.g. if it were a button, you would only get one
#   signal for the button depress, not for the button release.
# ----------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------
# Callback class recievers need to override.  Example in test below
# ----------------------------------------------------------------------------------------
class JukeboxSignalCallback(object):
    
    def Signalled(self):
        raise NotImplementedError()
        pass

# ----------------------------------------------------------------------------------------
# Class which checks for a button press, and calls back via the callback class to
# This runs on a seperate thread when the thread.start is called.
# ----------------------------------------------------------------------------------------
class JukeboxSignalReceiver(threading.Thread):

    # Are we listening to inputs
    run = True
    # Link to hardware
    hardware = None
    # Link to a calling class instance
    callback = None
    
    lastSignalTime = None
    
    def __init__(self, jukeboxCallback):
        super(JukeboxSignalReceiver, self).__init__()
        self.hardware = BreadBoardInput()
        self.callback = jukeboxCallback
	self.lastSignalTime = time.time()
     

    def run(self):
        
        # can happen on exceptions withe the board or no board can be found
        if self.hardware.IsInitialised() == False:
            logging.info( 'Hardware not ready for input so exiting')
            return

        JukeboxSignalReceiver.run = True
        logging.info( 'Now listening to jukebox inputs')
        
        currentSignalState = False
        
        while JukeboxSignalReceiver.run:
            # Key is signalled, and thats a new value, compared to other states.
            if self.hardware.KeyInputIsSignalled() and currentSignalState == False:
                if self.is_genuine_key_signal(True):
                    currentSignalState = True
                    self.callback.Signalled();
                    elapsed_time = time.time() - self.lastSignalTime
                    logging.info("Signalled time since last signal: %.3f" %elapsed_time)
                    self.lastSignalTime = time.time()
            
            # Key is no longer signalled, we reset state, but dont tell via callback
            elif not self.hardware.KeyInputIsSignalled() and currentSignalState == True:
                if self.is_genuine_key_signal(False):
                    currentSignalState = False
                 
 
    # This method is to reduce jitter in the signals.  If this is a genuine change in
    # signal state, we will see a constant True/False over a period of 200 checks ! 
    def is_genuine_key_signal(self, new_state):
        starting_time = time.time()
        elapsed_time = 0

        for i in range (100):
            if self.hardware.KeyInputIsSignalled()  != new_state: 
                elapsed_time = time.time() - starting_time
#               print ("FALSE INPUT SIGNAL check time recorded: %.3f" %elapsed_time)
                return False
        return True
        

    @staticmethod
    def stopProcessing():
        logging.info( 'stopping hardware input monitor')
        JukeboxSignalReceiver.run = False

#---------------------------------------------
# TEST MAIN METHOD
#---------------------------------------------
class TestSignalCallback(JukeboxSignalCallback):
    def Signalled(self):
        logging.info("Jukebox callback recieved")

if __name__ == "__main__":
    
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%m-%d %H:%M', filename='sonos-jukebox-server.log', filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)


    # Provides 10 seconds of key press feedback via the console.
    # ensures, with the sleep that this is all on a background thread.
    # After 10 seconds this auto stops
    cb = TestSignalCallback()
    ps = JukeboxSignalReceiver(cb)
    ps.start()
    sleep(10)
    ps.stopProcessing()
    ps.join()
    print 'ended'
