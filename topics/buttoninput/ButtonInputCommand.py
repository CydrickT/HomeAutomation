from typing import Final

from topics.buttoninput.ButtonInputType import ButtonInputType


class ButtonInputCommand:

    def __init__(self, buttoninputype=ButtonInputType.UpShort):
        self.buttonInputType: Final = buttoninputype

