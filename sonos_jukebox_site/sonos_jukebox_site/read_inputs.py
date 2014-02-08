import RPi.GPIO as GPIO
import datetime

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN)

on = False

lastSignalTime = None

while 1:
    if GPIO.input(7) and on == False:
        timeSinceLastSignal = datetime.datetime.now() - self.lastSignalTime
        print "%s Down" % timeSinceLastSignal.total_seconds() 
        on = True
        lastSignalTime = datetime.datetime.now()
    elif not GPIO.input(7) and on == True:
        on = False
        
 