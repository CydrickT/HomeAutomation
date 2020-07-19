from core.ConfigManager import ConfigManager
from core.DataRouter import DataRouter
from core.Logger import Logger
from core.ServiceManager import ServiceManager


class Core:
    def __init__(self, config):
        self.logger = Logger()
        self.dataRouter = DataRouter(self)
        self.serviceManager = ServiceManager(self, config)
        self.configManager = ConfigManager(config, self.serviceManager.services)

