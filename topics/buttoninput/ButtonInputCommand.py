from typing import Final

from topics.buttoninput.ButtonInputType import ButtonInputType


class ButtonInputCommand:

    def __init__(self, button_input_type=ButtonInputType.UpShort):
        self.button_input_type: Final = button_input_type

