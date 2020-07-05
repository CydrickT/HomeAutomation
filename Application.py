from core.Core import Core
from services.CommandInterpreterService import CommandInterpreterService
from services.LightManagerService import LightManagerService
from services.TerminalInputService import TerminalInputService


class Application:

    def __init__(self):
        self.__core = Core()

        self.__lightManagementService = LightManagerService(self.__core)
        self.__core.serviceManager.addService(self.__lightManagementService)

        self.__terminalInputService = TerminalInputService(self.__core)
        self.__core.serviceManager.addService(self.__terminalInputService)

        self.__commandInterpreterService = CommandInterpreterService(self.__core)
        self.__core.serviceManager.addService(self.__commandInterpreterService)

        self.__core.serviceManager.startServices()


app = Application()
