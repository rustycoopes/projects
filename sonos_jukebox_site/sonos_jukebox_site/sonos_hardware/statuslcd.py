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
    isScreenOn = True
    # link to the hardware
    lcd = None
    
    def __init__(self):
        super(LCDScreen, self).__init__()
        LCDScreen.lcd = Adafruit_CharLCDPlate()
        self.screenOff()
        logging.info('screen status manager created')
            

    @staticmethod
    def updateStatus(line1Text, line2Text):
        LCDScreen.lcd.clear()
        LCDScreen.lcd.message(line1Text + '\n' + line2Text)
        logging.info( 'Message set to "%s"' % line1Text)

    def screenOn(self):
        LCDScreen.lcd.backlight(LCDScreen.lcd.ON)
        LCDScreen.isScreenOn = True
        logging.info( 'LCD light turned on')

    def screenOff(self):
        LCDScreen.lcd.backlight(LCDScreen.lcd.OFF)
        LCDScreen.isScreenOn = False
        logging.info( 'LCD light turned off')
        
    # Purpose of the thread start is to capture button selections to turn light on and off.
    def run(self):
        logging.info( 'LCD screen on/off manager running')
        while 1:
            # Select pressed and screeen was already on
            if LCDScreen.lcd.buttonPressed(LCDScreen.lcd.SELECT) and LCDScreen.isScreenOn:
                self.screenOff()
            # Select pressed and screen was off !
            elif LCDScreen.lcd.buttonPressed(LCDScreen.lcd.SELECT) and LCDScreen.isScreenOn != True:
                self.screenOn()
            sleep (.25)   

    @staticmethod
    def stopProcessing():
        LCDScreen.lcd.clear()
        LCDScreen.lcd.backlight(LCDScreen.lcd.OFF)
        LCDScreen.isScreenOn = False
        logging.info( 'LCD light turned off')

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
    ps = LCDScreen()
    ps.screenOn()
    ps.start()
    sleep(1)
    LCDScreen.updateStatus("Key Pressed", "A1")
    sleep(1)
    LCDScreen.updateStatus("Searching Sonos", "Elton")
    sleep(1)
    LCDScreen.stopProcessing()
    ps.join()
    print 'ended'