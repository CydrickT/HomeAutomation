import json
from core.Service import Service
from topics.generalstate.GeneralStateChangeNotification import GeneralStateChangeNotification
from topics.generalstate.GeneralStateType import GeneralStateType
from libs.sshexecutor import SshExecutor
import time

class UnraidShutdownService(Service):

    def initialize(self):
        self.unraidInstancesToShutdown = json.loads(self.config['UnraidInstancesToShutdown'])
        self.core.dataRouter.subscribe(GeneralStateChangeNotification, self.handleStateChangeNotification)

    def handleStateChangeNotification(self, state_change_notification):
        if state_change_notification.general_state_type == GeneralStateType.SleepPreparation:
            for unraidInstanceToShutdown in self.unraidInstancesToShutdown:
                sshExecutor = SshExecutor(unraidInstanceToShutdown['hostname'], unraidInstanceToShutdown['username'], unraidInstanceToShutdown['passowrd'])
                time.sleep(1.0)
                sshExecutor.execute("powerdown")
                time.sleep(1.0)
                sshExecutor.close()
