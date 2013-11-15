import logging
import threading
from breadboardlights import BreadBoardLights
import RPi.GPIO as GPIO
from time import sleep

class ProgramStatus(object):
    NotRunning=0
    Waiting = 1
    ReceivedKeys = 2
    LoadingMusicInfo = 3
    CallingSonos = 4

class ProgramStatusManager(threading.Thread):

    run = True
    status = ProgramStatus.NotRunning
    breadBoard = None
    IOInitialised = False
    
    def __init__(self):
        super(ProgramStatusManager, self).__init__()
        try:
            self.breadBoard = BreadBoardLights()
            self.IOInitialised = True
        except:
            logging.error( 'GPIO Failed')
            

    @staticmethod
    def updateStatus(new_status):
        ProgramStatusManager.status = new_status
        logging.info( 'Status set to "%s"' % new_status)
    def run(self):
        
        if self.IOInitialised == False:
            return

        ProgramStatusManager.run = True
        logging.info( 'Hardware Status Manager running')
        while ProgramStatusManager.run:
            if ProgramStatusManager.status != ProgramStatus.NotRunning:
                self.breadBoard.RunningLight(False)

            if ProgramStatusManager.status == ProgramStatus.ReceivedKeys:
                self.breadBoard.RecievedKeysLight(False)
                self.breadBoard.LoadingMusicLight(True)
                self.breadBoard.CallSonosLight(True)
            elif ProgramStatusManager.status == ProgramStatus.LoadingMusicInfo:
                self.breadBoard.RecievedKeysLight(True)
                self.breadBoard.LoadingMusicLight(False)
                self.breadBoard.CallSonosLight(True)
            elif ProgramStatusManager.status == ProgramStatus.CallingSonos:
                self.breadBoard.RecievedKeysLight(True)
                self.breadBoard.LoadingMusicLight(True)
                self.breadBoard.CallSonosLight(False)
            sleep(.25)
            self.breadBoard.RunningLight(True)
            sleep(.25)

    @staticmethod
    def stopProcessing():
        logging.info( 'stopping hardware status monitor')
        ProgramStatusManager.run = False




if __name__ == "__main__":
    
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%m-%d %H:%M', filename='sonos-jukebox-server.log', filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    ProgramStatusManager.updateStatus(ProgramStatus.NotRunning)
    ps = ProgramStatusManager()
    ps.start()
    sleep(1)
    ProgramStatusManager.updateStatus(ProgramStatus.CallingSonos)
    sleep(1)
    ProgramStatusManager.updateStatus(ProgramStatus.ReceivedKeys)
    sleep(1)
    ProgramStatusManager.stopProcessing()
    ps.join()
    print 'ended'