from core.DataRouter import DataRouter
from core.Logger import Logger
from core.ServiceManager import ServiceManager


class Core:
    def __init__(self, config):
        self.dataRouter = DataRouter()
        self.logger = Logger()
        self.serviceManager = ServiceManager()
        self.configManager = ConfigManager()
