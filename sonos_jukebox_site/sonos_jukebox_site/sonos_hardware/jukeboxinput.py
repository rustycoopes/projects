import logging
import threading
from breadboardinputs import BreadBoardInput
import RPi.GPIO as GPIO
from time import sleep


class JukeboxSignalCallback(object):
    def Signalled(self):
        raise NotImplementedError()
        pass

class JukeboxSignalManager(threading.Thread):

    run = True
    breadBoard = None
    IOInitialised = False
    callback = None
    
    def __init__(self, jukeboxCallback):
        super(JukeboxSignalManager, self).__init__()
        try:
            self.breadBoard = BreadBoardInput()
            self.IOInitialised = True
            self.callback = jukeboxCallback
        except:
            logging.error( 'GPIO Failed')
            


    def run(self):
        
        if self.IOInitialised == False:
            return

        JukeboxSignalManager.run = True
        logging.info( 'Hardware Input Manager running')
        
        currentSignalState = False
        
        while JukeboxSignalManager.run:
            if self.breadBoard.KeyInputIsSignalled() and currentSignalState == False:
                currentSignalState = True
                self.callback.Signalled();
                logging.info("Breadboard Signal On")
            

            elif not self.breadBoard.KeyInputIsSignalled() and currentSignalState == True:
                currentSignalState = False
                logging.info("Breadboard Signal Off")
            
            
            sleep(.25)

    @staticmethod
    def stopProcessing():
        logging.info( 'stopping hardware input monitor')
        JukeboxSignalManager.run = False



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

    cb = TestSignalCallback()
    ps = JukeboxSignalManager(cb)
    ps.start()
    sleep(10)
    ps.stopProcessing()
    ps.join()
    print 'ended'