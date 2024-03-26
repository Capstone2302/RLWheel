import gym
import rospy
import roslaunch
import time
import numpy as np
from gym import utils, spaces
from gym_gazebo.envs import gazebo_env
from geometry_msgs.msg import Twist
from std_srvs.srv import Empty
from gym.utils import seeding
import copy
import math
import os

from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np
from sensor_msgs.msg import JointState
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from std_msgs.msg import Float64
from gazebo_msgs.srv import SetLinkState
from gazebo_msgs.msg import LinkState
import message_filters
from message_filters import ApproximateTimeSynchronizer, Subscriber
from gazebo_msgs.msg import ModelState 
from gazebo_msgs.msg import ModelStates
from gazebo_msgs.srv import SetModelState
from sensor_msgs.msg import Image
import csv
from rosgraph_msgs.msg import Clock
from datetime import datetime

from Controls.pid_controller import MotorController
from Controls.ball_detection import BallDetector
from Controls.uart_handlr import receive_msg, send_msg

class WheelEnvironment():
    def __init__(self):
        self.x_threshold = 50 # when when x is farther than THRESHOLD pixels from the center_pixel, reset
        self.y_threshold = 450 # when we is greater than this reset
        self.center_pixel = 399
        self.vel_threshold = 30
        self.n_actions = 1
        self.bridge = CvBridge()
        self.record = None
        self.net = None
        self.controller = None

        # Logging telemetry
        self.do_telemetry = False

        self.action_space = spaces.Discrete(self.n_actions) # output degrees 
        # cartesian product, 3 Dimensions - ball_pos_x, prev_pos_x, wheel_vel, dt
        high = np.array([ self.x_threshold, self.x_threshold, 1, 20])
        self.observation_space = spaces.Box(low=-high, high = high)

        self.ball_detector = BallDetector()
        # State data:
        self.ball_pos_x = None
        self.wheel_pos = None
        self.wheel_vel = 0
        self.ball_vel = None
        self.integral = 0
        self.prev_time = time.time()-1
        self.time = time.time()
        self.x_prev = 0
        self.y_prev = 0
        self.ball_pos_x_camera = -9999999
        self.ball_found = True

    def setNetwork(self, net):
        self.net = net
        self.controller = MotorController(net)

    def setRecordingState(self, record):
        self.record=record

    def get_wheel_vel_callback(self):
        delt_enc = receive_msg()
        diff_time = self.time - self.prev_time
        self.wheel_vel = (delt_enc * 60) / (diff_time * 2400)
        # print(msg.velocity)
        # self.wheel_vel = msg.velocity
        
        # print('wheel pos read: '+ str(self.wheel_pos))
        # self.wheel_pos_write = self.wheel_pos+1
        # self.joint_pub.publish(self.wheel_pos_write)
        # print('position published: '+ str(self.wheel_pos+1))

    def get_time(self):
        self.prev_time = self.time
        self.time = time.time()

    def get_ball_pos_camera_callback(self):
        self.ball_pos_x, self.ball_found = self.ball_detector.ball_finder(self.do_telemetry,display=True)
        self.ball_pos_x = - self.ball_pos_x

    def step(self, pwm_est):
        # publish action
        msg = str(int(pwm_est)).ljust(7, "\t")
        send_msg(msg)

        # get stat
        prev_found = self.ball_found
        self.get_ball_pos_camera_callback()
        self.get_wheel_vel_callback()
        
        self.get_time()
        dt = self.time - self.prev_time

        # Define state  
        state = [self.ball_pos_x, self.x_prev, dt, self.integral]

        self.x_prev = self.ball_pos_x
        
        # Check for end condition
        done = bool(not self.ball_found and not prev_found)
        reward = 1-abs(self.ball_pos_x)/self.x_threshold
        return state, reward, done, {}
    
    def reset(self): 
        print("**** RESETTING ****")
        msg = str(int(0)).ljust(7, "\t")
        send_msg(msg)
        time.sleep(1)
        print("Press the enter key to enable controller")
        key = input()
        while key.lower() != "":
            print("You didn't press space. Please try again.")
            key = input()
        print("enter key pressed, enabling controller")
        self.get_ball_pos_camera_callback()
        prev_pos = self.ball_pos_x
        print(prev_pos)
        self.get_time()
        self.get_ball_pos_camera_callback()
        self.get_wheel_vel_callback()
        self.get_time()
        state = [self.ball_pos_x, prev_pos,self.time-self.prev_time, self.integral]
        # Process state
        print("**** DONE RESET ****")
        return state