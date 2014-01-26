import RPi.GPIO as GPIO
import logging
# ----------------------------------------------------------------------
# Class Purpose
#   Provide abstraction from the GPIO setup and config - including pin.
#   Allos user just to ask for signal state.
# ----------------------------------------------------------------------
class BreadBoardInput(object):

    IOInitialised = False
    
    def __init__(self):
        super(BreadBoardInput, self).__init__()
        try:
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(7, GPIO.IN)
            self.IOInitialised = True
        except:
            logging.error('Error initialising GPIO for input %s' % sys.exc_info()[1])
            

    def IsInitialised(self):
        return self.IOInitialised

    
    def KeyInputIsSignalled(self):
         return GPIO.input(7)

