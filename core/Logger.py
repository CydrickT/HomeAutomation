import datetime
import sys
import traceback


class Logger:
    def log(self, message):
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": " + message)

    def logError(self, message, error):
        self.log(message)
        print(traceback.format_exception(None, error, error.__traceback__), file=sys.stderr, flush=True)
