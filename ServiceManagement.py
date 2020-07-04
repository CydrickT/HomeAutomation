class ServiceManagement:
    def __init__(self):
        self.services = []
    
    def addService(self, service):
        if not issubclass(type(service), Service)
             raise Exception('Group ' + groupName + ' not found.')
        self.services.append(service)
        service.initialize()
    