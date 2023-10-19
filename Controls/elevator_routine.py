#TODO: Update documentation
import RPi.GPIO as gpio
from time import sleep

SW = 22

DIR = 21
STEP = 20
CW =1
CCW =0

gpio.setmode(gpio.BCM)
gpio.setup(DIR, gpio.OUT)
gpio.setup(STEP, gpio.OUT)
gpio.output(DIR,CW)

gpio.setmode(gpio.BCM)
gpio.setup(SW, gpio.IN)

def homing_sequence():
        while(True):
            gpio.output(DIR,CW) #2300
            for x in range(50):
                gpio.output(STEP,gpio.HIGH)
                sleep(.00100)
                gpio.output(STEP,gpio.LOW)
                sleep(.00100)
            if gpio.input(SW):
                print("closed")
                break

def elevator_routine():
    gpio.output(DIR,CCW)
    for x in range(1900): #2300
        gpio.output(STEP,gpio.HIGH)
        sleep(.000500)
        gpio.output(STEP,gpio.LOW)
        sleep(.000500)
    for x in range(380): #2300
        gpio.output(STEP,gpio.HIGH)
        sleep(.00100)
        gpio.output(STEP,gpio.LOW)
        sleep(.00100)    
    sleep(0.2)
    gpio.output(DIR,CW) #2300
    for x in range(2335):
        gpio.output(STEP,gpio.HIGH)
        sleep(.00030)
        gpio.output(STEP,gpio.LOW)
        sleep(.00030)

        
#This will be called only wh
# en the IR sensor says there is a ball 

# do the routine for the stepper motor test, get to the top and then get to the bottom and wait to be called again 