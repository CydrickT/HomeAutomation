#!/usr/bin/python

# {"devicetype":"rpi#wakeup_sleep"}


import requests
import json
import datetime
import vlc
import RPi.GPIO as GPIO
import time
import configparser



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