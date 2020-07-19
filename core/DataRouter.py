import threading


class DataRouter:
    def __init__(self, core):
        self.__subscriberMap = {}
        self.core = core

    def publish(self, topic_instance):
        topicname = topic_instance.__class__.__name__
        if topicname in self.__subscriberMap:
            for callback in self.__subscriberMap[topicname]:
                try:
                    callbackthread = threading.Thread(target=callback(topic_instance))
                    callbackthread.start()
                except Exception as e:
                    self.core.logger.logError("An error occurred when sending " + topicname, e)

    def subscribe(self, topic, callback):
        topicName = topic.__name__
        if not topicName in self.__subscriberMap:
            self.__subscriberMap[topicName] = []
        self.__subscriberMap[topicName].append(callback)
