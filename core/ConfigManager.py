class ConfigManager:

    def __init__(self, config, services):
        configuration_map = self.build_configuration_map(config)
        self.add_config_to_service(configuration_map, services)

    def build_configuration_map(self, config):
        configMap = {}
        for sectionName in config.sections():
            indexOfEqual = sectionName.rfind('=')
            serviceId = sectionName[0:indexOfEqual]
            childKeys = config[sectionName]
            configMap[serviceId] = childKeys
        return configMap

    def add_config_to_service(self, configuration_map, services):
        for service in services.values():
            if service.id in configuration_map:
                service.config = configuration_map[service.id]


