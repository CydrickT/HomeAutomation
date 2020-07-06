from enum import Enum


class GeneralStateType(Enum):
    SleepPreparation = 1
    TrueSleep = 2
    GetOutOfBed = 3
    NightEmergency = 4