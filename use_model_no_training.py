#!/usr/bin/env python3
import gym
from gym import wrappers
import gym_gazebo
import time
#import numpy
import random
import time

import os.path
from os import path

import inspect

from collections import namedtuple
import numpy as np
from tensorboardX import SummaryWriter

from WheelEnvironment import WheelEnvironment

import torch
import torch.nn as nn
import torch.optim as optim
from datetime import datetime

# Logging dependencies
import cv2
import os
import signal
import sys
import shutil

HIDDEN_SIZE = 128 # number of neurons in hidden layer
BATCH_SIZE = 16   # number of episodes to play for every network iteration
PERCENTILE = 70   # only the episodes with the top 30% total reward are used 
                  # for training

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

        self.folderName = datetime.now().strftime("%b%d-%H-%M-%S-rlwheel")

    def forward(self, x):
        return self.net(x)


def iterate_batches(env, net, batch_size):
    obs = env.reset()

    while True:
        
        obs_v = torch.FloatTensor([obs])

        act_probs_v = (net(obs_v))

        action = float(act_probs_v[0])

        next_obs, reward, is_done, _ = env.step(action)

        if is_done:
            next_obs = env.reset()
            
        obs = next_obs



# Function to delete the entire output directory
def delete_output_directory(output_dir):
    try:
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
    except Exception as e:
        print(f"Error deleting directory {output_dir}: {e}")

if __name__ == '__main__':
    # Setup environment
    env = WheelEnvironment()
    obs_size = env.observation_space.shape[0]
    n_actions = env.action_space.n


    # Create the NN object
    net = Net(obs_size, HIDDEN_SIZE, n_actions)
    net.load_state_dict(torch.load('Models/Mar25-19-29-37-rlwheel.pth'))
    env.reset()
    # For every batch of episodes (BATCH_SIZE episodes per batch) we identify the
    # episodes in the top (100 - PERCENTILE) and we train our NN on them.
    iterate_batches(env, net, BATCH_SIZE)