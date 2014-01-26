import logging
import sys
import threading
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
    
    def __init__(self, jukeboxCallback):
        super(JukeboxSignalReceiver, self).__init__()
        self.hardware = BreadBoardInput()
        self.callback = jukeboxCallback
 

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
                currentSignalState = True
                self.callback.Signalled();
                logging.info("Breadboard Signal On")
            
            # Key is no longer signalled, we reset state, but dont tell via callback
            elif not self.hardware.KeyInputIsSignalled() and currentSignalState == True:
                currentSignalState = False
                logging.info("Breadboard Signal Off")


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