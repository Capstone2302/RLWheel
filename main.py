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
import _thread
import time
import RPi.GPIO as gpio

from Controls.reset_mechanism import reset_mechanism
from RL.camera_setup import display

def main():
    """
    The main entry point of the application.

    More detailed information about what the main function does goes here,
    explaining its purpose and overall program flow.

    """
    # Your main program logic goes here
    
    x = _thread.start_new_thread(display,())
    reset_mechanism()


if __name__ == "__main__":
   main()