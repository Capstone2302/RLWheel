import RPi.GPIO as gpio
#from elevator_routine import elevator_routine

IR = 16


gpio.setmode(gpio.BCM)
gpio.setup(IR, gpio.IN)

def reset_mechanism():
    try:
        while(True):
                print(gpio.input(IR))
                if (gpio.input(IR) == True):
                    print("elevator routine placeholder")
                # elevator_routine()

    except KeyboardInterrupt: # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
        gpio.cleanup()
        print("Cleaning up!")