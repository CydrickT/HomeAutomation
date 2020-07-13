import threading
import importlib

from core.Service import Service


class ServiceManager:

    def __init__(self, core, config):
        self.core = core
        self.services = {}
        self.readConfigFile(config)

    def readConfigFile(self, config):
        for sectionName in config.sections():
            indexOfLastPoint = sectionName.rfind('.')
            indexOfEqual = sectionName.rfind('=')
            serviceId = sectionName[0:indexOfEqual]
            moduleName = sectionName[indexOfEqual + 1:indexOfLastPoint]
            className = sectionName[indexOfLastPoint + 1:len(sectionName)]
            self.instantiateService(moduleName, className, serviceId)

    def instantiateService(self, module_name, class_name, service_id):
        self.core.logger.log("Instantiating Module: " + module_name + ", Class: " + class_name + ", ID: " + service_id)
        reflectedModule = importlib.import_module(module_name)
        reflectedClass = getattr(reflectedModule, class_name)
        serviceInstance = reflectedClass()
        self.addService(serviceInstance, service_id)

    def addService(self, service, service_id):
        if not issubclass(type(service), Service):
             raise Exception('Class \'' + type(service).__name__ + '\' does not extend from \'' + type(service).__name__ + '\'')
        elif service_id in self.services:
            raise Exception('Service ID ' + service + ' already exists.')
        service.core = self.core
        service.id = service_id
        self.services[service_id] = service

    def initializeServices(self):
        for service in self.services.values():
            initservicethread = threading.Thread(target=service.initialize)
            initservicethread.start()

    def startServices(self):
        for service in self.services.values():
            startservicethread = threading.Thread(target=service.start)
            startservicethread.start()