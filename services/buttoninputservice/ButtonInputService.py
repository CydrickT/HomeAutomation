import configparser
import json
import time
from datetime import datetime, timedelta
import RPi.GPIO as GPIO

from core.Service import Service
from topics.buttoninput.ButtonInputCommand import ButtonInputCommand
from topics.buttoninput.ButtonInputType import ButtonInputType


class ButtonInputService(Service):

    def initialize(self):
        self.button_up_gpio_id = self.config.getint('ButtonUpGpioId')
        self.button_down_gpio_id = self.config.getint('ButtonDownGpioId')
        self.shortToLongThresholdInSeconds = self.config.getfloat('ShortToLongThresholdInSeconds')

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.button_up_gpio_id, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.button_down_gpio_id, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def start(self):
        upCurrentlyPressed = False
        downCurrentlyPressed = False
        signalSent = False
        timeDown = None
        while True:
            upPressed = False
            downPressed = False
            if GPIO.input(self.button_up_gpio_id) == GPIO.HIGH:
                upPressed = True
            if GPIO.input(self.button_down_gpio_id) == GPIO.HIGH:
                downPressed = True

            if upPressed:  # TODO Move this condition
                if not upCurrentlyPressed and not signalSent:
                    # New Up pressed. Resetting time and registering that it's currently down.

                    upCurrentlyPressed = True
                    timeDown = datetime.now()

            if downPressed:  # TODO Move this condition.
                if not downCurrentlyPressed and not signalSent:
                    # New Up pressed. Resetting time and registering that it's currently down.
                    downCurrentlyPressed = True
                    timeDown = datetime.now()

            if not signalSent:
                if timeDown + timedelta(seconds=self.shortToLongThresholdInSeconds) < datetime.now():
                    # We have crossed the short to long threshold. It's now considered a long press.
                    buttonInputType = None
                    if upCurrentlyPressed and downCurrentlyPressed:
                        buttonInputType = ButtonInputType.UpDownLong
                    elif upCurrentlyPressed:
                        buttonInputType = ButtonInputType.UpLong
                    elif downCurrentlyPressed:
                        buttonInputType = ButtonInputType.DownLong

                    self.core.dataRouter.publish(ButtonInputCommand(buttonInputType))
                    signalSent = True

                elif upCurrentlyPressed and not upPressed:
                    # Up was recently released, but was less than threshold. Considered a short button press.
                    buttonInputType = ButtonInputType.UpShort
                    if downCurrentlyPressed:
                        # Was a short 2-button input
                        buttonInputType = ButtonInputType.UpDownShort

                    self.core.dataRouter.publish(ButtonInputCommand(buttonInputType))
                    signalSent = True

                elif downCurrentlyPressed and not downPressed:
                    # Down was recently released, but was less than threshold. Considered a short button press.
                    buttonInputType = ButtonInputType.DownShort
                    if upCurrentlyPressed:
                        # Was a short 2-button input
                        buttonInputType = ButtonInputType.UpDownShort

                    self.core.dataRouter.publish(ButtonInputCommand(buttonInputType))
                    signalSent = True

            if not upPressed and not downPressed:
                # Waiting until both buttons are released to fully reset everything.
                signalSent = False
                timedown = None

            time.sleep(0.01)
