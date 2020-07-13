import configparser
import sys

from core.Core import Core
from services.commandinterpreterservice.CommandInterpreterService import CommandInterpreterService
from services.lightmanagerservice.LightManagerService import LightManagerService
from services.musicmanagementservice.MusicManagerService import MusicManagerService
from services.terminalinputservice.TerminalInputService import TerminalInputService
from services.wakeonlanmanagerservice.WakeOnLanManagerService import WakeOnLanManagerService


class Application:

    def __init__(self):

        config = configparser.ConfigParser()
        config.read(sys.argv[1])

        self.__core = Core(config)
        self.__core.serviceManager.initializeServices()
        self.__core.serviceManager.startServices()


app = Application()

