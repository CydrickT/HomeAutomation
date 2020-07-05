import datetime


class Logger:
    def log(self, message):
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": " + message)
