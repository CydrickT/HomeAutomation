from core.Service import Service
from topics.ButtonInput import ButtonInput
from topics.ButtonInputType import ButtonInputType


class TerminalInputService(Service):

    def start(self):
        print('Write the following commands to the console:\n    LongNextButton\n    LongPreviousButton\n    '
              'ShortNextButton\n    ShortPreviousButton\n    ShortBothButton\n    LongBothButton')
        while True:
            i = input('Command:')
            self.core.dataRouter.publish(ButtonInput(ButtonInputType.UpLong))

