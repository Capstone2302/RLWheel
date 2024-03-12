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
from Controls.ball_detection import BallDetector
import time

# Define the serial port and its settings
# ser = serial.Serial("/dev/ttyUSB0", baudrate=115200, stopbits=1, timeout=100)
ser = 10
print("serial port set up")
controller = MotorController()
log_perhaps = True


def main():
    """
    The main entry point of the application.

    More detailed information about what the main function does goes here,
    explaining its purpose and overall program flow.

    """
    ball_detector = BallDetector()
    prev_ball_image_time = time.time()

    try:
        while True:
            err = ball_detector.ball_finder(log_perhaps)
            print("Loop processing time: " + str(time.time() - prev_ball_image_time))
            prev_ball_image_time = time.time()
            # controller.control_routine(ser,err, log_perhaps)

    except KeyboardInterrupt:
        # Handle Ctrl+C to exit gracefully
        print("\nScript terminated by user.")

    finally:
        controller.exit(ser, log_perhaps)
        ball_detector.exit(log_perhaps)


if __name__ == "__main__":
    main()
