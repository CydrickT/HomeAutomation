from topics.generalstate.GeneralStateType import GeneralStateType


class GeneralStateChangeNotification:

    def __init__(self, general_state_type=GeneralStateType.SleepPreparation):
        self.general_state_type = general_state_type

