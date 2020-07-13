import configparser
import json
from datetime import datetime, time
from typing import Final
import RPi.GPIO as GPIO

from core.Service import Service

class ButtonInputService(Service):

    def initialize(self):
        self.button_up_gpio_id = self.config['ButtonUpGpioId']
        self.button_down_gpio_id = self.config['ButtonDownGpioId']

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.button_up_gpio_id, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.button_down_gpio_id, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def start(self):
        upPressed = False
        downPressed = False
        signalSent = False
        timeDown = None
        while True:
            if GPIO.input(self.button_up_gpio_id) == GPIO.HIGH:
                upPressed = True
            if GPIO.input(self.button_down_gpio_id) == GPIO.HIGH:
                downPressed = True

            if (upPressed or downPressed) and timeDown == None:
                self.core.logger.log("Up pressed? " + str(upPressed) + ", Down Pressed? " + str(downPressed))
                    timeDown = datetime.datetime.now()
            elif timeDown != None:
                timeDown = None
            time.sleep(0.05)