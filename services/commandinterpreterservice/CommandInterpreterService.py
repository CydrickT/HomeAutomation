from typing import Final

from core.Service import Service
from topics.buttoninput.ButtonInputCommand import ButtonInputCommand
from topics.buttoninput.ButtonInputType import ButtonInputType
from topics.generalstate.GeneralStateChangeNotification import GeneralStateChangeNotification
from topics.generalstate.GeneralStateType import GeneralStateType
from topics.modifierstate.ModifierStateChangeNotification import ModifierStateChangeNotification
from topics.modifierstate.ModifierType import ModifierType


class CommandInterpreterService(Service):

    def __init__(self):
        self.state = GeneralStateType.GetOutOfBed

    def initialize(self):
        self.core.dataRouter.subscribe(ButtonInputCommand, self.handleButtonInput)

    # States:
    # 1- Going to sleep: Stop lights, start music
    # 2- True sleep: Close music
    # 3- Wakeup: Turn on lights, Change lights scene, wake computer up
    def handleButtonInput(self, buttonInput):
        self.core.logger.log('Previous state: ' + str(self.state))
        if buttonInput.button_input_type == ButtonInputType.UpLong:
            self.state = self.getForwardMovingState(self.state)
            self.core.logger.log('Next state: ' + str(self.state))
            self.core.dataRouter.publish(GeneralStateChangeNotification(self.state))
        elif buttonInput.button_input_type == ButtonInputType.DownLong:
            self.state = self.getBackwardMovingState(self.state)
            self.core.logger.log('Next state: ' + str(self.state))
            self.core.dataRouter.publish(GeneralStateChangeNotification(self.state))
        elif buttonInput.button_input_type == ButtonInputType.UpDownLong:
            self.state = GeneralStateType.NightEmergency
            self.core.logger.log('Next state: ' + str(self.state))
            self.core.dataRouter.publish(GeneralStateChangeNotification(self.state))
        elif buttonInput.button_input_type == ButtonInputType.UpShort:
            self.core.logger.log('Modifier Up pressed')
            self.core.dataRouter.publish(ModifierStateChangeNotification(ModifierType.Increase))
        elif buttonInput.button_input_type == ButtonInputType.DownShort:
            self.core.logger.log('Modifier Down pressed')
            self.core.dataRouter.publish(ModifierStateChangeNotification(ModifierType.Decrease))

    def getForwardMovingState(self, previousState):
        if previousState == GeneralStateType.GetOutOfBed:
            return GeneralStateType.SleepPreparation
        elif previousState == GeneralStateType.SleepPreparation:
            return GeneralStateType.TrueSleep
        elif previousState == GeneralStateType.TrueSleep:
            return GeneralStateType.GetOutOfBed
        elif previousState == GeneralStateType.NightEmergency:
            return GeneralStateType.TrueSleep

    def getBackwardMovingState(self, previousState):
        if previousState == GeneralStateType.GetOutOfBed:
            return GeneralStateType.TrueSleep
        elif previousState == GeneralStateType.SleepPreparation:
            return GeneralStateType.GetOutOfBed
        elif previousState == GeneralStateType.TrueSleep:
            return GeneralStateType.SleepPreparation
        elif previousState == GeneralStateType.NightEmergency:
            return GeneralStateType.TrueSleep
