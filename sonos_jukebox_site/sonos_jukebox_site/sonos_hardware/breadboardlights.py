import RPi.GPIO as GPIO

class BreadBoardLights(object):

    def __init__(self):
        super(BreadBoardLights, self).__init__()
        GPIO.setup(13, GPIO.OUT)
        GPIO.setup(15, GPIO.OUT)
        GPIO.setup(16, GPIO.OUT)
        GPIO.setup(18, GPIO.OUT)

    def RunningLight(on):
         GPIO.output(18, on)

    def RecievedKeysLight(on):
        GPIO.output(13, on)

    def LoadingMusicLight(on):
        GPIO.output(15, on)

    def CallSonosLight(on):
        GPIO.output(16, on)
