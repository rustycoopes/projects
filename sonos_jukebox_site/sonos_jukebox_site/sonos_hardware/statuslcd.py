import logging
import sys
import threading
import RPi.GPIO as GPIO
from time import sleep
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate

class ProgramStatusScreenManager(threading.Thread):

    screenOn = True
    lcd = None
    IOInitialised = False
    
    def __init__(self):
        super(ProgramStatusScreenManager, self).__init__()
        self.lcd = Adafruit_CharLCDPlate()
        self.lcd.clear()
        self.lcd.backlight(lcd.OFF)
        ProgramStatusScreenManager.screenOn = False
        logging.info('screen status manager created')
            

    @staticmethod
    def updateStatus(line1Text, line2Text):
        self.lcd.clear()
        self.lcd.message(line1Text + '\n' + line2Text)
        logging.info( 'Message set to "%s"' % line1Text, line2Text)
    
    def run(self):
        logging.info( 'Hardware Status Manager running')
        while 1:
            if self.lcd.buttonPressed(lcd.SELECT) && ProgramStatusScreenManager.screenOn:
                self.lcd.backlight(lcd.OFF)
                ProgramStatusScreenManager.screenOn = True
            elif lcd.buttonPressed(lcd.SELECT) && ProgramStatusScreenManager.screenOn != True:
                self.lcd.backlight(lcd.ON)
                ProgramStatusScreenManager.screenOn = False
            sleep(.25)

    @staticmethod
    def stopProcessing():
        logging.info( 'stopping hardware status monitor')
        self.lcd.clear()
        self.lcf.backlight(lcd.OFF)
        ProgramStatusScreenManager.screenOn = False




if __name__ == "__main__":
    
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%m-%d %H:%M', filename='sonos-jukebox-server.log', filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    ProgramStatusManager.updateStatus("Running", "")
    ps = ProgramStatusManager()
    ps.start()
    sleep(1)
    ProgramStatusManager.updateStatus("Key Pressed", "A1")
    sleep(1)
    ProgramStatusManager.updateStatus("Searching Sonos", "Elton")
    sleep(1)
    ProgramStatusManager.stopProcessing()
    ps.join()
    print 'ended'