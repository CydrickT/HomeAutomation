#!/usr/bin/python
from topics.generalstate.GeneralStateChangeNotification import GeneralStateChangeNotification
from topics.generalstate.GeneralStateType import GeneralStateType


x = GeneralStateChangeNotification
print(x.__name__)

y = GeneralStateChangeNotification(GeneralStateType.TrueSleep)
print(y.__class__.__name__)