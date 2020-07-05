from typing import Final

from core.Service import Service
from topics.ButtonInput import ButtonInput


class CommandInterpreterService(Service):

    def initialize(self):
        self.core.dataRouter.subscribe(ButtonInput(), self.handleButtonInput)

    def handleButtonInput(self, buttonInput):
        print("RECEIVED COMAMND: " + str(buttonInput.buttonInputType))