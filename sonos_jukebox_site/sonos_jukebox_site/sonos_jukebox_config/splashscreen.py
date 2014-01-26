
import logging

from sonos_hardware.statuslcd import LCDScreen
from time import sleep


# ----------------------------------------------------------------------------------------
# Class purpose
#    To act as the splash screen on start up
#    IMPORTANTLY this has a side effect of performing screen intitialisation as its the only part
#    of the program that creads an LCD screen instance, and therefore calls the constructor
# ----------------------------------------------------------------------------------------

class SplashScreen(object):

    lcd = None
    
    def __init__(self):
        self.lcd = LCDScreen()
        self.lcd.start()

    def ShowSplash(self):
        self.lcd.screenOn()
        LCDScreen.updateStatus("Sonos Jukebox", "Russ Cooper")
        sleep(1)
        LCDScreen.updateStatus("Sonos Jukebox", "Starting....")
        sleep(1)

