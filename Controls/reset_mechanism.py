import RPi.GPIO as gpio
from elevator_routine import elevator_routine

IR = 16

def reset_mechanism():
    while(True):
            if (gpio.input(IR) == False):
                print("elevator routine placeholder")
               # elevator_routine()
