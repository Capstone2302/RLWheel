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

# TODO: import tenserflow or torch of some kind
from Controls.pid_controller import MotorController
from Controls.ball_detection import BallDetector
import time


log_perhaps = True


def main():
    """
    The main entry point of the application.

    More detailed information about what the main function does goes here,
    explaining its purpose and overall program flow.

    """
    ball_detector = BallDetector()

    try:
        wait_for_space()
        net = torch.load("file path where model lives")
        controller = MotorController(net)
        while True:
            err, reset_integrator = ball_detector.ball_finder(log_perhaps, display=True)
            # model takes in inputs, err, derivative or error (both of ball position from set point), dt
            controller.control_routine(
                err, log_perhaps
            )  # TODO: re implement the reset integrator term

    except KeyboardInterrupt:
        # Handle Ctrl+C to exit gracefully
        print("\nScript terminated by user.")

    finally:
        controller.exit(log_perhaps)
        ball_detector.exit(log_perhaps)


def wait_for_space():
    print("Press the enter key to enable controller")
    key = input()
    while key.lower() != "":
        print("You didn't press space. Please try again.")
        key = input()
    print("enter key pressed, enabling controller")


if __name__ == "__main__":
    main()
