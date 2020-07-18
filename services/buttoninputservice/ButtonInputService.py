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

        self.button_state_manager = ButtonStateManager(self.config.getfloat('ShortToLongThresholdInSeconds'))

        self.enableLightFeedback = self.config.getboolean('EnableLightFeedback')
        self.light_up_gpio_id = self.config.getint('LightUpGpioId')
        self.light_down_gpio_id = self.config.getint('LightDownGpioId')

        self.setupBoard()


    def setupBoard(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.button_up_gpio_id, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.button_down_gpio_id, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        if self.enableLightFeedback:
            GPIO.setup(self.light_up_gpio_id, GPIO.OUT, initial=GPIO.LOW)
            GPIO.setup(self.light_down_gpio_id, GPIO.OUT, initial=GPIO.LOW)


    def start(self):

        while True:
            time.sleep(0.01)
            self.button_state_manager.resetCycle()

            if GPIO.input(self.button_up_gpio_id) == GPIO.HIGH:
                self.button_state_manager.up_currently_pressed = True
            if GPIO.input(self.button_down_gpio_id) == GPIO.HIGH:
                self.button_state_manager.down_currently_pressed = True

            if not self.button_state_manager.signalSent:
                if self.button_state_manager.isConsideredLongPress():
                    # We have crossed the short to long threshold. It's now considered a long press.
                    self.longPressDetected()

                elif self.button_state_manager.upRecentlyReleased():
                    # Up was recently released, but was less than threshold. Considered a short button press.
                    self.shortUpReleased()

                elif self.button_state_manager.downRecentlyReleased():
                    # Down was recently released, but was less than threshold. Considered a short button press.
                    self.shortDownReleased()
            elif self.button_state_manager.bothButtonsCurrentlyReleased():
                self.setLightState(False, False)

    def longPressDetected(self):
        buttonInputType = None

        if self.button_state_manager.bothButtonsPreviouslyPressed():
            buttonInputType = ButtonInputType.UpDownLong
            self.setLightState(True, True)
        elif self.button_state_manager.up_previously_pressed:
            buttonInputType = ButtonInputType.UpLong
            self.setLightState(True, False)
        elif self.button_state_manager.down_previously_pressed:
            buttonInputType = ButtonInputType.DownLong
            GPIO.output(self.light_down_gpio_id, GPIO.HIGH)
            self.setLightState(False, True)

        self.sendSignal(buttonInputType)

    def shortUpReleased(self):
        buttonInputType = ButtonInputType.UpShort
        if self.button_state_manager.down_previously_pressed:
            # Was a short 2-button input
            buttonInputType = ButtonInputType.UpDownShort

        self.sendSignal(buttonInputType)

    def shortDownReleased(self):
        buttonInputType = ButtonInputType.DownShort
        if self.button_state_manager.up_previously_pressed:
            # Was a short 2-button input
            buttonInputType = ButtonInputType.UpDownShort

        self.sendSignal(buttonInputType)

    def sendSignal(self, buttonInputType):
        self.core.dataRouter.publish(ButtonInputCommand(buttonInputType))
        self.button_state_manager.signalSent = True

    def setLightState(self, lightUpOn, lightDownOn):
        if self.enableLightFeedback:
            lights = (self.light_up_gpio_id, self.light_down_gpio_id)
            upValue = GPIO.HIGH if lightUpOn else GPIO.LOW
            downValue = GPIO.HIGH if lightDownOn else GPIO.LOW
            values = (upValue, downValue)
            GPIO.output(lights, values)


class ButtonStateManager:

    def __init__(self, short_to_long_threshold_in_seconds):
        self.up_previously_pressed = False
        self.down_previously_pressed = False
        self.up_currently_pressed = False
        self.down_currently_pressed = False
        self.signalSent = False
        self.timeDown = None
        self.__short_to_long_threshold_in_seconds__ = short_to_long_threshold_in_seconds

    def resetCycle(self):

        if self.upRecentlyPressed() and not self.signalSent:
            self.timeDown = datetime.now()

        if self.downRecentlyPressed() and not self.signalSent:
            self.timeDown = datetime.now()

        if not self.up_currently_pressed and not self.down_currently_pressed and self.signalSent:
            # Waiting until both buttons are released to fully reset everything.
            self.signalSent = False
            self.timeDown = None

        self.up_previously_pressed = self.up_currently_pressed
        self.down_previously_pressed = self.down_currently_pressed

        self.up_currently_pressed = False
        self.down_currently_pressed = False

    def isConsideredLongPress(self):
        return self.timeDown is not None and self.timeDown + timedelta(seconds=self.__short_to_long_threshold_in_seconds__) < datetime.now()

    def upRecentlyPressed(self):
        return self.up_currently_pressed and not self.up_previously_pressed

    def downRecentlyPressed(self):
        return self.down_currently_pressed and not self.down_previously_pressed

    def upRecentlyReleased(self):
        return not self.up_currently_pressed and self.up_previously_pressed

    def downRecentlyReleased(self):
        return not self.down_currently_pressed and self.down_previously_pressed

    def bothButtonsCurrentlyPressed(self):
        return self.up_currently_pressed and self.down_currently_pressed

    def bothButtonsCurrentlyReleased(self):
        return not self.up_currently_pressed and not self.down_currently_pressed

    def bothButtonsPreviouslyPressed(self):
        return self.up_currently_pressed and self.down_currently_pressed

