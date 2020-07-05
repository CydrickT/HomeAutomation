from typing import Final


class Service:

    def __init__(self, core):
        self.core: Final = core

    def initialize(self):
        pass

    def start(self):
        pass
