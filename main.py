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
import logging
import threading
import time
import RPi.GPIO as gpio

from Controls.reset_mechanism import reset_mechanism
from RL.camera_setup import display
def thread_function(name):
    logging.info("Thread %s: starting", name)
    time.sleep(2)
    logging.info("Thread %s: finishing", name)

def main():
    """
    The main entry point of the application.

    More detailed information about what the main function does goes here,
    explaining its purpose and overall program flow.

    """
    # Your main program logic goes here\
    try:
        x = threading.Thread(target= display())
        y = threading.Thread(target= reset_mechanism())

        x.start()
        y.start()

    except KeyboardInterrupt: # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
        gpio.cleanup()
        x._Thread_stop()
        y._Thread_stop()
        print("Cleaning up!")


if __name__ == "__main__":
   main()