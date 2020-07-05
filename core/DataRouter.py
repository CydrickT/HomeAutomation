import threading


class DataRouter:
    def __init__(self):
        self.__subscriberMap = {}

    def publish(self, topicinstance):
        topicname = type(topicinstance).__name__
        if topicname in self.__subscriberMap:
            for callback in self.__subscriberMap[topicname]:
                callbackthread = threading.Thread(target=callback(topicinstance))
                callbackthread.start()


    def subscribe(self, topic, callback):
        topicName = type(topic).__name__
        if not topicName in self.__subscriberMap:
            self.__subscriberMap[topicName] = []
        self.__subscriberMap[topicName].append(callback)
