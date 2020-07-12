from typing import Final

from core.Service import Service
from topics.buttoninput.ButtonInputCommand import ButtonInputCommand
from topics.buttoninput.ButtonInputType import ButtonInputType


class TerminalInputService(Service):

    def start(self):
        self.core.logger.log('Write the following commands to the console:\n    UpLong\n    DownLong\n    '
              'UpShort\n    DownShort\n    UpDownShort\n    UpDownLong')
        while True:
            i = input('Command:')
            button_input_type = None
            if i == 'UpLong':
                button_input_type = ButtonInputType.UpLong
            elif i == 'DownLong':
                button_input_type = ButtonInputType.DownLong
            elif i == 'UpShort':
                button_input_type = ButtonInputType.UpShort
            elif i == 'DownShort':
                button_input_type = ButtonInputType.DownShort
            elif i == 'UpDownShort':
                button_input_type = ButtonInputType.UpDownShort
            elif i == 'UpDownLong':
                button_input_type = ButtonInputType.UpDownLong

            if button_input_type is None:
                self.core.logger.log('Command ' + str(button_input_type) + ' is invalid.')
            else:
                self.core.dataRouter.publish(ButtonInputCommand(button_input_type))
