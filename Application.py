from core.Core import Core
from services.commandinterpreterservice.CommandInterpreterService import CommandInterpreterService
from services.lightmanagementservice.LightManagerService import LightManagerService
from services.terminalinputservice.TerminalInputService import TerminalInputService
from services.wakeonlanmanagerservice.WakeOnLanManagerService import WakeOnLanManagerService


class Application:

    def __init__(self):
        self.__core = Core()

        self.__core.serviceManager.addService(LightManagerService(self.__core))
        self.__core.serviceManager.addService(TerminalInputService(self.__core))
        self.__core.serviceManager.addService(CommandInterpreterService(self.__core))
        self.__core.serviceManager.addService(WakeOnLanManagerService(self.__core))

        self.__core.serviceManager.startServices()

app = Application()
