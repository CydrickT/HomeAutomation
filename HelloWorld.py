#!/usr/bin/python


import RPi.GPIO as GPIO


buttonUp = 10
buttonDown = 12

def setupButtons():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(buttonUp, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(buttonDown, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


setupButtons()

while True:
    if GPIO.input(buttonUp) == GPIO.HIGH:
        print("UP PRESSED")
    if GPIO.input(buttonDown) == GPIO.HIGH:
        print("DOWN PRESSED")