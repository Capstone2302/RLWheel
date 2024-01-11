"""
main.py

This is the main module of the RL Wheel Project

Description:
This module contains the main entry point of the application and orchestrates
the overall program flow.

Usage:
- Run this module to start the application.

Author:
Ashli Forbes

Date:
Created - 06/10/2023
"""

# Imports
import serial
from Controls.pid_controller import MotorController 
from Controls.uart_handlr import send_msg
from Controls.ball_detection import BallDetector

# Define the serial port and its settings
ser = serial.Serial('/dev/ttyUSB0', baudrate=115200, stopbits=1, timeout=100) 
controller = MotorController()
log_perhaps = True

def main():
    """
    The main entry point of the application.

    More detailed information about what the main function does goes here,
    explaining its purpose and overall program flow.

    """
    count = 0
    ball_detector = BallDetector()

    try:
        while True:

            # run control loop
            if count<500 or count>1000:
                controller.control_routine(ser,50, log_perhaps)
            else:
                controller.control_routine(ser,-50, log_perhaps)
            count +=1
            print(count)


    except KeyboardInterrupt:
        # Handle Ctrl+C to exit gracefully
        print("\nScript terminated by user.")


    finally:  
        controller.exit(ser, log_perhaps)

if __name__ == "__main__":
    main()