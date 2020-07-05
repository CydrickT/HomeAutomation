from typing import Final

from topics.ButtonInputType import ButtonInputType


class ButtonInput:

    def __init__(self, buttoninputype=ButtonInputType.UpShort):
        self.buttonInputType: Final = buttoninputype

