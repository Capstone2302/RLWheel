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
        wait_for_space()
        while True:
            err, reset_integrator = ball_detector.ball_finder(log_perhaps, display=True)
            if reset_integrator:
                controller.send_pwm_val(0)
                time.sleep(1)

                controller.control_routine(0, reset_integrator, log_perhaps)
                wait_for_space()
                reset_integrator = False
                continue
            controller.control_routine(err, reset_integrator, log_perhaps)

    except KeyboardInterrupt:
        # Handle Ctrl+C to exit gracefully
        print("\nScript terminated by user.")

    finally:
        controller.exit(log_perhaps)
        ball_detector.exit(log_perhaps)


def wait_for_space():
    print("Press the enter key to enable controller")
    key = input()
    while key.lower() != '':
        print("You didn't press space. Please try again.")
        key = input()
    print("enter key pressed, enabling controller")


if __name__ == "__main__":
    main()
