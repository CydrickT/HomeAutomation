from typing import Final
import os


class Service:

    def __init__(self, core):
        self.core: Final = core

#    def __build_configuration(self):
#        filename = type(self).__name__ + '.config'
#        if (os.path.isfile(filename))
#            self.config =

    def initialize(self):
        pass

    def start(self):
        pass