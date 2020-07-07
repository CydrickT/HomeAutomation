from typing import Final

from core.Service import Service
from topics.buttoninput.ButtonInputCommand import ButtonInputCommand
from topics.buttoninput.ButtonInputType import ButtonInputType
from topics.generalstate.GeneralStateChangeNotification import GeneralStateChangeNotification
from topics.generalstate.GeneralStateType import GeneralStateType
from topics.modifierstate.ModifierStateChangedNotification import ModifierStateChangedNotification
from topics.modifierstate.ModifierType import ModifierType


class CommandInterpreterService(Service):

    def __init__(self, core):
        self.core: Final = core
        self.state = GeneralStateType.GetOutOfBed

    def initialize(self):
        self.core.dataRouter.subscribe(ButtonInputCommand(), self.handleButtonInput)

    # States:
    # 1- Going to sleep: Stop lights, start music
    # 2- True sleep: Close music
    # 3- Wakeup: Turn on lights, Change lights scene, wake computer up
    def handleButtonInput(self, buttonInput):
        if buttonInput.buttoninputype == ButtonInputType.UpLong:
            self.state = self.getForwardMovingState(self.state)
            self.core.dataRouter.publish(GeneralStateChangeNotification(self.state))
        elif buttonInput.buttoninputype == ButtonInputType.DownLong:
            self.state = self.getBackwardMovingState(self.state)
            self.core.dataRouter.publish(GeneralStateChangeNotification(self.state))
        elif buttonInput.buttoninputype == ButtonInputType.UpDownLong:
            self.state = GeneralStateType.NightEmergency
            self.core.dataRouter.publish(GeneralStateChangeNotification(self.state))
        elif buttonInput.buttoninputype == ButtonInputType.UpShort:
            self.dataRouter.publish(ModifierStateChangedNotification(ModifierType.Increase))
        elif buttonInput.buttoninputype == ButtonInputType.DownShort:
            self.dataRouter.publish(ModifierStateChangedNotification(ModifierType.Decrease))

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
