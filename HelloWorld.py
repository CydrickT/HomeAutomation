#!/usr/bin/python

# {"devicetype":"rpi#wakeup_sleep"}


import requests
import json
import datetime
import vlc
import RPi.GPIO as GPIO
import time
import configparser

def isAllOnInGroup(ip, username, groupId):
    group = apiGet(ip, username, 'groups/' + str(groupId))
    allOn = group['state']['all_on']
    log("Are all lights opened on group " + groupId + "? " + str(allOn))
    return allOn

def getSceneIdByName(ip, username, sceneName):
    scenes = apiGet(ip, username, 'scenes')
    for scene in scenes:
        log('Found scene named ' + scenes[scene]['name'] + '. Its ID is ' + scene) 
        if scenes[scene]['name'] == sceneName:
            return scene;
    raise Exception('Scene ' + sceneName + ' not found.')
            

def getLightsInGroup(ip, username, groupId):
    group = apiGet(ip, username, 'groups/' + str(groupId))
    lights = group['lights']
    log("Lights in group " + groupId + ": " + str(lights))
    return lights
    
    
def getGroupIdFromGroupName(ip, username, groupName):
    log("Looking for group named " + groupName)
    groups = apiGet(ip, username, 'groups')
    for group in groups:
        log("Found group named " + groups[group]['name'] + ". Its ID is " + group)
        if groups[group]['name'] == groupName:
            return group
    raise Exception('Group ' + groupName + ' not found.')

def turnOnOffGroup(ip, username, groupId, isOn):
    content = {'on': isOn}
    response = apiPut(ip, username, 'groups/' + groupId + '/action', content)
        
def setSceneInGroup(ip, username, groupId, sceneName):
    sceneId = getSceneIdByName(ip, username, sceneName)
    content = {'scene' : sceneId}
    response = apiPut(ip, username, 'groups/' + groupId + '/action', content)
    

def apiGet(ip, username, request):
    url = 'http://' + ip + '/api/' + username + '/' + request
    log("Doing GET request on " + url)
    resp = requests.get(url)
    if resp.status_code != 200:
        raise ApiError('GET failed: ' + response.status_code)
    log("Response on GET request is " + str(resp.status_code) + ":\n" + str(resp.json()))
    return resp.json();

def apiPut(ip, username, request, content):
    url = 'http://' + ip + '/api/' + username + '/' + request
    jsonContent = json.dumps(content)
    log("Doing PUT request on " + url + " with JSON " + str(jsonContent))
    resp = requests.put(url, jsonContent)
    if resp.status_code != 200:
        raise ApiError('GET failed: ' + response.status_code)
    log("Response on PUT request is " + str(resp.status_code) + ":\n" + str(resp.json()))
    return resp.json();

def log(message):
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": " + message)
    
def playMusic(path):
    p = vlc.MediaPlayer(path)
    p.play()
    
    
def setupButtons():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(buttonUp, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(buttonDown, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    

config = configparser.ConfigParser()
config.read('HomeAutomationConfig.secret')
ip = config['PhilipsHue']['IP']
username = config['PhilipsHue']['Username']
groupName = config['PhilipsHue']['GroupName']
daytimeSceneName = config['PhilipsHue']['DaytimeSceneName']
nighttimeSceneName = config['PhilipsHue']['NighttimeSceneName']
musicPath = config['Music']['MusicPath']
buttonUp = 10
buttonDown = 12

MUSIC_NIGHTTIME = 1
TRUE_NIGHTTIME = 2
TURNING_ON_LIGHTS = 3
DAYTIME = 4

volumeToLightThresholdMillis = 750

state = 4

setupButtons()

timeDown = None

#while True:
#   upPressed = False
#    downPressed = False
#    if GPIO.input(buttonUp) == GPIO.HIGH:
#        upPressed = True
#    if GPIO.input(buttonDown) == GPIO.HIGH:
#        downPressed = True
#        
#    if upPressed or downPressed:
#        log("Up pressed? " + str(upPressed) + ", Down Pressed? " + str(downPressed))
#        if timeDown == None:
#            timeDown = datetime.datetime.now()
#        elif (timeDown + datetime.timedelta(milliseconds = volumeToLightThresholdMillis)) < datetime.datetime.now():
#            log("Here")
#    elif timeDown != None:
#        # Up and down are up, but there was a time where the buttons are down. 
#        log("Here")
#    time.sleep(0.05)
        

groupId = getGroupIdFromGroupName(ip, username, groupName)
isAllOn = isAllOnInGroup(ip, username, groupId)
print(getSceneIdByName(ip, username, nighttimeSceneName))
turnOnOffGroup(ip, username, groupId, not isAllOn)
#setSceneInGroup(ip, username, groupId, daytimeSceneName)
#playMusic(musicPath)