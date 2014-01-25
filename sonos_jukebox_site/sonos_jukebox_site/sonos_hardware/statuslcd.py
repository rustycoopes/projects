import logging
import sys
import threading
import RPi.GPIO as GPIO
from time import sleep
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate


# ----------------------------------------------------------------------------------------
# Class Purpose
#   Provides an interface into the LCD.  Able to turn on and off, and write text.
#   Thread is created to recieve the button presses to turn on and off the light.
# ----------------------------------------------------------------------------------------
class LCDScreen(threading.Thread):

    # State of the light, we cannot ask the hardware this
    screenOn = True
    # link to the hardware
    lcd = None
    
    def __init__(self):
        super(LCDScreen, self).__init__()
        self.lcd = Adafruit_CharLCDPlate()
        self.lcd.clear()
        self.lcd.backlight(lcd.OFF)
        LCDScreen.screenOn = False
        logging.info('screen status manager created')
            

    @staticmethod
    def updateStatus(line1Text, line2Text):
        self.lcd.clear()
        self.lcd.message(line1Text + '\n' + line2Text)
        logging.info( 'Message set to "%s"' % line1Text, line2Text)

    def screenOn(self):
        self.lcd.clear()
        self.lcd.backlight(lcd.ON)
        LCDScreen.screenOn = True
        logging.info( 'LCD light turned on')

    def screenOff(self):
        self.lcd.clear()
        self.lcd.backlight(lcd.OFF)
        LCDScreen.screenOn = False
        logging.info( 'LCD light turned off')
        
    # Purpose of the thread start is to capture button selections to turn light on and off.
    def run(self):
        logging.info( 'Hardware Status Manager running')
        while 1:
            # Select pressed and screeen was already on
            if self.lcd.buttonPressed(lcd.SELECT) and LCDScreen.screenOn:
                self.lcd.backlight(lcd.OFF)
                LCDScreen.screenOn = True
            # Select pressed and screen was off !
            elif lcd.buttonPressed(lcd.SELECT) and LCDScreen.screenOn != True:
                self.lcd.backlight(lcd.ON)
                LCDScreen.screenOn = False
          

    @staticmethod
    def stopProcessing():
        logging.info( 'stopping hardware status monitor')
        self.lcd.clear()
        self.lcf.backlight(lcd.OFF)
        LCDScreen.screenOn = False


#---------------------------------------------
# TEST MAIN METHOD
#---------------------------------------------
if __name__ == "__main__":
    
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%m-%d %H:%M', filename='sonos-jukebox-server.log', filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    # Just write out some text and and ensure the thread start works to accept button presses
    # 3 SECONDS TO CAPTURE USER SELECTS!!!
    ProgramStatusManager.updateStatus("Running", "")
    ps = ProgramStatusManager()
    ps.screenOn()
    ps.start()
    sleep(1)
    ProgramStatusManager.updateStatus("Key Pressed", "A1")
    sleep(1)
    ProgramStatusManager.updateStatus("Searching Sonos", "Elton")
    sleep(1)
    ProgramStatusManager.stopProcessing()
    ps.join()
    print 'ended'