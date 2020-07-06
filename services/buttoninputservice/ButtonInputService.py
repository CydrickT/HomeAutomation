from datetime import datetime, time
from typing import Final
import RPi.GPIO as GPIO

from core.Service import Service

buttonUp = 10
buttonDown = 12

class ButtonInputService(Service):


    def __init__(self, core):
        self.core: Final = core

    def initialize(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(buttonUp, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(buttonDown, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def start(self):
        while True:
            upPressed = False
            downPressed = False
            if GPIO.input(buttonUp) == GPIO.HIGH:
                upPressed = True
            if GPIO.input(buttonDown) == GPIO.HIGH:
                downPressed = True

            if upPressed or downPressed:
                self.core.logger.log("Up pressed? " + str(upPressed) + ", Down Pressed? " + str(downPressed))
                if timeDown == None:
                    timeDown = datetime.datetime.now()

            elif timeDown != None:
                # Up and down are up, but there was a time where the buttons are down.
                self.core.logger.log("Here")
            time.sleep(0.05)