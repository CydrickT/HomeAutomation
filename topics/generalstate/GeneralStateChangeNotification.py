from typing import Final

from topics.generalstate.GeneralStateType import GeneralStateType


class GeneralStateChangeNotification:

    def __init__(self, general_state_type=GeneralStateType.SleepPreparation):
        self.general_state_type: Final = general_state_type

