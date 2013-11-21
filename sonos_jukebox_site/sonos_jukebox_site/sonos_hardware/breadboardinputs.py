import RPi.GPIO as GPIO

class BreadBoardInput(object):

    def __init__(self):
        super(BreadBoardInput, self).__init__()
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(11, GPIO.IN)
    
    def KeyInputIsSignalled(self):
         return GPIO.input(11)

