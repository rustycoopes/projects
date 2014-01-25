import RPi.GPIO as GPIO

# ----------------------------------------------------------------------
# Class Purpose
#   Provide abstraction from the GPIO setup and config - including pin.
#   Allows user to toggle names lights on and off.
# ----------------------------------------------------------------------
class BreadBoardLights(object):

    def __init__(self):
        super(BreadBoardLights, self).__init__()
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(13, GPIO.OUT)
        GPIO.setup(15, GPIO.OUT)
        GPIO.setup(16, GPIO.OUT)
        GPIO.setup(18, GPIO.OUT)

    def RunningLight(self, on):
         GPIO.output(18, on)

    def RecievedKeysLight(self, on):
        GPIO.output(13, on)

    def LoadingMusicLight(self, on):
        GPIO.output(15, on)

    def CallSonosLight(self, on):
        GPIO.output(16, on)
