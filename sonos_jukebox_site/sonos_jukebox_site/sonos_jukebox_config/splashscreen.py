'''
Created on Oct 19, 2013

@author: rusty
'''
import logging

from sonos_hardware.statuslcd import ProgramStatusScreenManager
from time import sleep

class SplashScreen(object):

    statusManager = None
    
    def __init__(self):
        self.statusManager = ProgramStatusScreenManager()
        self.statusManager.start()

    def ShowSplash(self):
        ProgramStatusScreenManager.updateStatus("Sonos Jukebox", "Russ Cooper")
        sleepe(1)
        ProgramStatusScreenManager.updateStatus("Sonos Jukebox", "Starting....")
        sleep(1)

