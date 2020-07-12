import threading


class DataRouter:
    def __init__(self):
        self.__subscriberMap = {}

    def publish(self, topic_instance):
        topicname = topic_instance.__class__.__name__
        if topicname in self.__subscriberMap:
            for callback in self.__subscriberMap[topicname]:
                callbackthread = threading.Thread(target=callback(topic_instance))
                callbackthread.start()


    def subscribe(self, topic, callback):
        topicName = topic.__name__
        if not topicName in self.__subscriberMap:
            self.__subscriberMap[topicName] = []
        self.__subscriberMap[topicName].append(callback)
