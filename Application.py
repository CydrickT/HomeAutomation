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
        self.notifySystemd()
        self.__core__.serviceManager.startServices()

    def notifySystemd(self):
        try:
            import systemd.daemon
            systemd.daemon.notify('READY=1')
            self.__core__.logger.log('Systemd notified that app is started.')
        except Exception:
            self.__core__.logger.log('Could not load systemd.daemon')


app = Application()

