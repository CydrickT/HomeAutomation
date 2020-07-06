import configparser

from core.Service import Service
import struct
import socket

from topics.generalstate.GeneralStateChangeNotification import GeneralStateChangeNotification
from topics.generalstate.GeneralStateType import GeneralStateType

class WakeOnLanManagerService(Service):

    def WakeOnLanManagerService(self):
        self.config = configparser.ConfigParser()
        self.config.read('WakeOnLanManagerService.config')

    def initialize(self):
        self.core.dataRouter.subscribe(GeneralStateChangeNotification(), self.handleStateChangeNotification)

    def handleStateChangeNotification(self, stateChangeNotification):
        if stateChangeNotification == GeneralStateType.GetOutOfBed:



    def wakeOnLan(self, mac_address, broadcast_ip_address):
        # Construct 6 byte hardware address
        add_oct = mac_address.split(':')

        hwa = struct.pack('BBBBBB', int(add_oct[0], 16),
                          int(add_oct[1], 16),
                          int(add_oct[2], 16),
                          int(add_oct[3], 16),
                          int(add_oct[4], 16),
                          int(add_oct[5], 16))

        msg = '\xff' * 6 + hwa * 16

        soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        soc.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        soc.sendto(msg, (broadcast_ip_address, self.config.))
        soc.close()
