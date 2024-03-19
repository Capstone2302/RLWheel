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
import torch
import torch.nn as nn
import torchvision.models as models

log_perhaps = True

class Net(nn.Module):
    '''
    @brief Takes an observation from the environment and outputs a probability 
           for each action we can take.
    '''
    def __init__(self, obs_size, hidden_size, n_actions):
        super(Net, self).__init__()

        # Define the NN architecture
        #
        # REMINDER:
        # as the last layer outputs raw numerical values instead of 
        # probabilities, when we later in the code use the network to predict
        # the probabilities of each action  we need to pass the raw NN results 
        # through a SOFTMAX to get the probabilities.
        self.net = nn.Sequential(
            nn.Linear(obs_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, n_actions)
        )

    def forward(self, x):
        return self.net(x)

def main():
    """
    The main entry point of the application.

    More detailed information about what the main function does goes here,
    explaining its purpose and overall program flow.

    """
    ball_detector = BallDetector()

    num_obs = 3
    num_acts = 1
    HIDDEN_SIZE = 128
    net = Net(num_obs,HIDDEN_SIZE,num_acts) # forward pass args: pos, prev_pos, delta time
    net.load_state_dict(torch.load('Models/Mar07-15-56-28-rlwheel.pth'))
    net.eval()
    print("Model mounted in eval mode")

    try:
        wait_for_space()
        controller = MotorController(net)
        while True:
            err, reset_integrator = ball_detector.ball_finder(log_perhaps, display=True)
            # model takes in inputs, err, derivative or error (both of ball position from set point), dt
            controller.control_routine(err, log_perhaps) # TODO: re implement the reset integrator term

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
