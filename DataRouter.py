class DataRouter:
    def __init__(self):
        self.subscriberMap = {}
        
    def publish(self, topicInstance):
        topicName = type(topic).__name__
        for callback in subscriberMap[topicName]
            callback(topicInstance)
        
    def subscribe(self, topic, callback):
        topicName = type(topic).__name__
        if not topicName in self.subscriberMap:
            self.subscriberMap[topicName] = [] 
        self.subscriberMap[topicName].append(callback)
    