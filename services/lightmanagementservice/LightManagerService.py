import configparser
import json

import requests

from core.Service import Service
from topics.generalstate.GeneralStateChangeNotification import GeneralStateChangeNotification
from topics.generalstate.GeneralStateType import GeneralStateType


class LightManagerService(Service):

    def __init__(self, core):
        config = configparser.ConfigParser()
        config.read('LightManagerService.config')
        self.hue_bridge_IP = json.loads(config['ServiceSpecific']['HueBridgeIp'])
        self.hue_bridge_username = json.loads(config['ServiceSpecific']['HueBridgeUsername'])
        self.lights_group_name = json.loads(config['ServiceSpecific']['GroupName'])
        self.daytime_scene_name = json.loads(config['ServiceSpecific']['DaytimeSceneName'])
        self.nighttime_scene_name = json.loads(config['ServiceSpecific']['NighttimeSceneName'])

    def initialize(self):
        self.core.dataRouter.subscribe(GeneralStateChangeNotification(), self.handleStateChangeNotification)

    def handleStateChangeNotification(self, state_change_notification):
        if state_change_notification.general_state_type == GeneralStateType.SleepPreparation:
            groupId = self.getGroupIdFromGroupName(self.hue_bridge_IP, self.hue_bridge_username, self.lights_group_name)
            self.turnOnOffGroup(self.hue_bridge_IP, self.hue_bridge_username, groupId, False)
        elif state_change_notification.general_state_type == GeneralStateType.GetOutOfBed or state_change_notification.general_state_type == GeneralStateType.NightEmergency:
            groupId = self.getGroupIdFromGroupName(self.hue_bridge_IP, self.hue_bridge_username, self.lights_group_name)
            self.turnOnOffGroup(self.hue_bridge_IP, self.hue_bridge_username, groupId, True)

            sceneId = self.getSceneIdByName(self.hue_bridge_IP, self.hue_bridge_username, self.daytime_scene_name)
            self.setSceneInGroup(self.hue_bridge_IP, self.hue_bridge_username, groupId, sceneId)

    def isAllOnInGroup(self, ip, username, groupId):
        group = self.apiGet(ip, username, 'groups/' + str(groupId))
        allOn = group['state']['all_on']
        self.core.logger.log("Are all lights opened on group " + groupId + "? " + str(allOn))
        return allOn

    def getSceneIdByName(self, ip, username, sceneName):
        scenes = self.apiGet(ip, username, 'scenes')
        for scene in scenes:
            self.core.logger.log('Found scene named ' + scenes[scene]['name'] + '. Its ID is ' + scene)
            if scenes[scene]['name'] == sceneName:
                return scene;
        raise Exception('Scene ' + sceneName + ' not found.')

    def getLightsInGroup(self, ip, username, groupId):
        group = self.apiGet(ip, username, 'groups/' + str(groupId))
        lights = group['lights']
        self.core.logger.log("Lights in group " + groupId + ": " + str(lights))
        return lights

    def getGroupIdFromGroupName(self, ip, username, groupName):
        self.core.logger.log("Looking for group named " + groupName)
        groups = self.apiGet(ip, username, 'groups')
        for group in groups:
            self.core.logger.log("Found group named " + groups[group]['name'] + ". Its ID is " + group)
            if groups[group]['name'] == groupName:
                return group
        raise Exception('Group ' + groupName + ' not found.')

    def turnOnOffGroup(self, ip, username, groupId, isOn):
        content = {'on': isOn}
        response = self.apiPut(ip, username, 'groups/' + groupId + '/action', content)


    def setSceneInGroup(self, ip, username, groupId, sceneId):
        content = {'scene': sceneId}
        response = self.apiPut(ip, username, 'groups/' + groupId + '/action', content)

    def apiGet(self, ip, username, request):
        url = 'http://' + ip + '/api/' + username + '/' + request
        self.core.logger.log("Doing GET request on " + url)
        resp = requests.get(url)
        if resp.status_code != 200:
            raise Exception('GET failed: ' + resp.status_code)
        self.core.logger.log("Response on GET request is " + str(resp.status_code) + ":\n" + str(resp.json()))
        return resp.json();

    def apiPut(self, ip, username, request, content):
        url = 'http://' + ip + '/api/' + username + '/' + request
        jsoncontent = json.dumps(content)
        self.core.logger.log("Doing PUT request on " + url + " with JSON " + str(jsoncontent))
        resp = request.put(url, jsoncontent)
        if resp.status_code != 200:
            raise Exception('GET failed: ' + resp.status_code)
        self.core.logger.log("Response on PUT request is " + str(resp.status_code) + ":\n" + str(resp.json()))
        return resp.json();
