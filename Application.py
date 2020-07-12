import configparser

from core.Core import Core
from services.commandinterpreterservice.CommandInterpreterService import CommandInterpreterService
from services.lightmanagerservice.LightManagerService import LightManagerService
from services.musicmanagementservice.MusicManagerService import MusicManagerService
from services.terminalinputservice.TerminalInputService import TerminalInputService
from services.wakeonlanmanagerservice.WakeOnLanManagerService import WakeOnLanManagerService


class Application:

    def __init__(self):

        config = configparser.ConfigParser()
        configuration = config.read('HomeAutomation.config')

        self.__core = Core(configuration)

        #self.__core.serviceManager.addService(LightManagerService(self.__core))
        self.__core.serviceManager.addService(TerminalInputService(self.__core))
        self.__core.serviceManager.addService(CommandInterpreterService(self.__core))
        self.__core.serviceManager.addService(MusicManagerService(self.__core))
        #self.__core.serviceManager.addService(WakeOnLanManagerService(self.__core))

        self.__core.serviceManager.startServices()

app = Application()
