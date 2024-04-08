"""
pid_controller.py 

Description:
Class that runs and abstracts the PID control loop of the motor

Usage:
- Is called from other aspects of the program to output the PWM 

Author:
Ashli Forbes

Date:
Created - 03/12/2023
"""
import time
from .uart_handlr import receive_msg, send_msg
from .data_logger import DataLogger
from .encoder_processor import EncoderProcesser
import numpy as np


class MotorController:  # add class definitions
    def __init__(self):
        self.k_p = 3  # 2.25  # 4.5
        self.k_i = 0  # 1.5
        self.k_d = 0  # 0.5  # 2.8
        self.k_w = 0  # -2.9
        self.integrator_val = 0
        self.start_time = time.time()
        self.e_prev = 0
        self.wheel_error = 0
        self.logger = DataLogger()
        self.encoder = EncoderProcesser()
        self.r = None  # TODO
        self.state = 0

    # core functions

    def init_position(self):
        self.encoder.set_center_pos()
        print(self.encoder.curr_pos_rad)

    def receive_delt_enc(self):
        return receive_msg()

    def send_pwm_val(self, pwm_val):
        msg = str(int(pwm_val)).ljust(7, "\t")
        if send_msg(msg):
            return True
        else:
            return False

    # control functions

    def stabilize(self, ball_pos, log):
        print("in stabilize mode")

        self.state += 1

    def tilt(self, ball_pos, log):
        self.WheelPosPID(0.35, ball_pos, log)
        print("tilting")
        print(ball_pos)
        if ball_pos > 30:
            self.state += 1

    def up_yank(self, ball_pos, log):
        self.BallPosPID(ball_pos, log)
        print("yank up")
        if ball_pos < 6:
            self.state = 0

    def catch_ball(self, ball_pos, log):
        print("catching ball")
        self.WheelPosPID(np.pi, ball_pos, log)
        # if ball_pos < 6:
        #     self.state = 0

    # main control loop

    def control_routine(self, ball_pos, log):
        self.start_time = time.time()
        # if self.state == 0:
        #     self.stabilize(ball_pos, log)
        # elif self.state == 1:
        #     self.tilt(ball_pos, log)
        # elif self.state == 2:
        #     self.catch_ball(ball_pos, log)
        # # elif self.state == 3:
        # #     self.catch_ball(ball_pos, log)

        self.encoder.delt_to_rad(receive_msg())

    # tuned utility functions

    def BallPosPID(self, curr_pos, log):
        # get encoder value from UART
        curr_time = time.time()
        diff_time = curr_time - self.start_time
        self.start_time = curr_time
        delt_enc = receive_msg()
        diff_pos = 0 - curr_pos  # set_rpm - curr_rpm
        wheel_pos = self.encoder.delt_to_rad(delt_enc)
        # using PID variables and such, calculate PWM output
        self.integrator_val += self.e_prev * diff_time

        pwm_kp = self.k_p * diff_pos
        pwm_ki = self.k_i * (self.integrator_val)
        pwm_kd = self.k_d * (diff_pos - self.e_prev) / diff_time
        pwm_est = pwm_kp + pwm_ki + pwm_kd
        self.e_prev = diff_pos
        self.send_pwm_val(pwm_est)
        if log:
            self.logger.log_data(
                delt_enc,
                diff_time,
                curr_pos,
                0,
                time.time(),
                pwm_kp,
                pwm_ki,
                pwm_kd,
                wheel_pos,
                curr_pos,
            )

    def WheelPosPID(self, set_pos, ball_pos, log):
        k_p = 100
        k_i = 1
        k_d = 0
        if set_pos > np.pi * 2:
            print("over 2 pi input")

        diff_time = time.time() - self.start_time
        delt_enc = receive_msg()
        curr_pos = self.encoder.delt_to_rad(delt_enc)

        # using PID variables and such, calculate PWM output
        self.integrator_val += self.wheel_error * diff_time
        error = set_pos - curr_pos
        if abs(error) > np.pi:
            error = error - 2 * np.pi * np.copysign(1, error)

        diff_pos = error

        pwm_kp = k_p * diff_pos
        pwm_ki = k_i * (self.integrator_val)
        pwm_kd = k_d * (self.wheel_error - diff_pos) / diff_time
        pwm_est = pwm_kp + pwm_ki + pwm_kd
        self.wheel_error = diff_pos

        self.send_pwm_val(pwm_est)
        if log:
            self.logger.log_data(
                delt_enc,
                diff_time,
                diff_pos,
                set_pos,
                time.time(),
                pwm_kp,
                pwm_ki,
                pwm_kd,
                curr_pos,
                ball_pos,
            )

    def exit(self, log):
        msg = str(0).ljust(7, "\t")
        send_msg(msg)
        if log:
            print("trying to write")
            self.logger.write_file()
