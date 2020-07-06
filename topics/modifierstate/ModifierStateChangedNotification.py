from typing import Final

from topics.modifierstate.ModifierType import ModifierType


class ModifierStateChangedNotification:

    def __init__(self, modifier_type=ModifierType.Increase):
        self.modifier_type: Final = modifier_type
