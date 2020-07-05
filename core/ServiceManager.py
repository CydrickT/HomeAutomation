import threading

from core.Service import Service


class ServiceManager:
    def __init__(self):
        self.services = []
    
    def addService(self, service):
        if not issubclass(type(service), Service):
             raise Exception('Class \'' + type(service).__name__ + '\' does not extend from \'' + type(service).__name__ + '\'')
        self.services.append(service)

        initservicethread = threading.Thread(target=service.initialize)
        initservicethread.start()

    def startServices(self):
        for service in self.services:
            startservicethread = threading.Thread(target=service.start)
            startservicethread.start()