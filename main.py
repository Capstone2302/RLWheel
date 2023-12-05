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
import time
import pandas as pd 
from pathlib import Path 
from Controls.pid_controller import MotorController #TODO: import properly
from Controls.uart_handlr import send_msg
from Controls.ball_detection import BallDetector

# Define the serial port and its settings
# ser = serial.Serial('/dev/ttyUSB0', baudrate=115200, stopbits=1, timeout=100) 
controller = MotorController()
def main():
    """
    The main entry point of the application.

    More detailed information about what the main function does goes here,
    explaining its purpose and overall program flow.

    """

    ball_detector = BallDetector();

    try:
        while True:

            # run control loop
            # controller.control_routine(ser,40)
            ball_detector.control_routine()
            print("in")


    except KeyboardInterrupt:
        # Handle Ctrl+C to exit gracefully
        print("\nScript terminated by user.")


    finally:  

        msg = str(0).ljust(7, '\t')
        # send_msg(ser, msg)
        # ser.close()


    

if __name__ == "__main__":
    main()