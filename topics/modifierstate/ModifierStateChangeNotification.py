from topics.modifierstate.ModifierType import ModifierType


class ModifierStateChangeNotification:

    def __init__(self, modifier_type=ModifierType.Increase):
        self.modifier_type = modifier_type
