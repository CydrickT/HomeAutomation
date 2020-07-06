from core.Service import Service
from topics.buttoninput.ButtonInputCommand import ButtonInputCommand
from topics.generalstate.GeneralStateType import GeneralStateType


class CommandInterpreterService(Service):

    # States:
    # 1- Going to sleep: Stop lights, start music
    # 2- True sleep: Close music
    # 3- Wakeup: Turn on lights, Change lights scene, wake computer up

    def initialize(self):
        self.core.dataRouter.subscribe(ButtonInputCommand(), self.handleButtonInput)
        self.state = GeneralStateType.GetOutOfBed

    def handleButtonInput(self, buttonInput):
        if buttonInput.buttoninputype == ButtonInputType.UpLong:
