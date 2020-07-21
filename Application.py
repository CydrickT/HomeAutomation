import configparser
import sys
import importlib

from core.Core import Core

class Application:

    def __init__(self):

        config = configparser.ConfigParser()
        config.read(sys.argv[1])

        self.__core__ = Core(config)
        self.__core__.serviceManager.initializeServices()
        self.__core__.serviceManager.startServices()


app = Application()

