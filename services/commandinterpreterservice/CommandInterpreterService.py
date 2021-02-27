import datetime

from core.Service import Service
from topics.buttoninput.ButtonInputCommand import ButtonInputCommand
from topics.buttoninput.ButtonInputType import ButtonInputType
from topics.generalstate.GeneralStateChangeNotification import GeneralStateChangeNotification
from topics.generalstate.GeneralStateType import GeneralStateType
from topics.modifierstate.ModifierStateChangeNotification import ModifierStateChangeNotification
from topics.modifierstate.ModifierType import ModifierType


class CommandInterpreterService(Service):

    def initialize(self):
        self.state = GeneralStateType.GetOutOfBed
        self.smartBedtimeManagementEnabled = self.config.getboolean('SmartBedtimeManagementEnabled')
        self.sbmMinHours = int(self.config['SmartBedtimeManagementMinTime'].split(':')[0])
        self.sbmMinMinutes = int(self.config['SmartBedtimeManagementMinTime'].split(':')[1])
        self.sbmMaxHours = int(self.config['SmartBedtimeManagementMaxTime'].split(':')[0])
        self.sbmMaxMinutes = int(self.config['SmartBedtimeManagementMaxTime'].split(':')[1])

        self.core.dataRouter.subscribe(ButtonInputCommand, self.handleButtonInput)

    # States:
    # 1- Going to sleep: Stop lights, start music
    # 2- True sleep: Close music
    # 3- Wakeup: Turn on lights, Change lights scene, wake computer up
    def handleButtonInput(self, buttonInput):
        self.core.logger.log('Previous state: ' + str(self.state))
        if buttonInput.button_input_type == ButtonInputType.UpLong:
            now = datetime.datetime.now()
            sbmMinTime = now.replace(hour=self.sbmMinHours, minute=self.sbmMinMinutes, second=0, microsecond=0)
            sbmMaxTime = now.replace(hour=self.sbmMaxHours, minute=self.sbmMaxMinutes, second=0, microsecond=0)
            if self.smartBedtimeManagementEnabled and (now > sbmMaxTime or now < sbmMinTime) and self.state == GeneralStateType.TrueSleep:
                # This is a special case. In the morning, the state never got to GetOutOfBed, it never left TrueSleep.
                # However, now is the evening and we're attempting to move forward. We want to go to SleepPreparation.
                # Setting the state to GetOutOfBed temporarily, knowing that it's going to get to the next state
                # after GetOutOfBed outside this condition.
                self.core.logger.log('State was previously TrueSleep but we are between min and max sbm time. ' +
                                     'Setting state temporarily to GetOutOfBed')
                self.state = GeneralStateType.GetOutOfBed
            self.state = self.getForwardMovingState(self.state)
            self.core.logger.log('Next state: ' + str(self.state))
            self.core.dataRouter.publish(GeneralStateChangeNotification(self.state))
        elif buttonInput.button_input_type == ButtonInputType.DownLong:
            self.state = self.getBackwardMovingState(self.state)
            self.core.logger.log('Next state: ' + str(self.state))
            self.core.dataRouter.publish(GeneralStateChangeNotification(self.state))
        elif buttonInput.button_input_type == ButtonInputType.UpDownLong:
            if self.state == GeneralStateType.NightEmergency:
                self.state = self.getForwardMovingState(self.state)
            else:
                self.state = GeneralStateType.NightEmergency
            self.core.logger.log('Next state: ' + str(self.state))
            self.core.dataRouter.publish(GeneralStateChangeNotification(self.state))
        elif buttonInput.button_input_type == ButtonInputType.UpShort:
            self.core.logger.log('Modifier Up pressed')
            self.core.dataRouter.publish(ModifierStateChangeNotification(ModifierType.Increase))
        elif buttonInput.button_input_type == ButtonInputType.DownShort:
            self.core.logger.log('Modifier Down pressed')
            self.core.dataRouter.publish(ModifierStateChangeNotification(ModifierType.Decrease))

    def getForwardMovingState(self, previousState):
        if previousState == GeneralStateType.GetOutOfBed:
            return GeneralStateType.SleepPreparation
        elif previousState == GeneralStateType.SleepPreparation:
            return GeneralStateType.TrueSleep
        elif previousState == GeneralStateType.TrueSleep:
            return GeneralStateType.GetOutOfBed
        elif previousState == GeneralStateType.NightEmergency:
            return GeneralStateType.TrueSleep

    def getBackwardMovingState(self, previousState):
        if previousState == GeneralStateType.GetOutOfBed:
            return GeneralStateType.TrueSleep
        elif previousState == GeneralStateType.SleepPreparation:
            return GeneralStateType.GetOutOfBed
        elif previousState == GeneralStateType.TrueSleep:
            return GeneralStateType.SleepPreparation
        elif previousState == GeneralStateType.NightEmergency:
            return GeneralStateType.TrueSleep
