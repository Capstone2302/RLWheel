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
        self.k_p = 3 # 2.25  # 4.5
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
        
    def tilt(self, ball_pos,dt, log):
        # self.WheelPosPID(0.0628,ball_pos,log)
        self.send_pwm_val(50)
        print(ball_pos)
        if ball_pos > 30:
            self.state += 1
            # time.sleep(1000)
        # if log:
        #     self.l
        # ogger.log_data(
        #         0,
        #         dt,
        #         ball_pos,
        #         0,
        #         0,
        #         0,
        #         60,
        #         0,
        #         0,
        #         ball_pos,
        #     )
            
    def up_yank(self, ball_pos,dt, log):
        # self.WheelPosPID(0.0628,ball_pos,log)
        self.BallPosPID(ball_pos,log)
        print("tilt")
        if ball_pos < 6:
            self.state += 1
            # time.sleep(1000)
        # if log:
        #     self.l
        # ogger.log_data(
        #         0,
        #         dt,
        #         ball_pos,
        #         0,
        #         0,
        #         0,
        #         60,
        #         0,
        #         0,
        #         ball_pos,
        #     )
            
    
    def control_routine(self, ball_pos, log):
        current_time = time.time()
        dt = current_time - self.start_time
        self.start_time = current_time
        self.prev_time = current_time
        if self.state == 0:
            # self.stabalize(ball_pos, dt,log)
            self.tilt(ball_pos,dt, log)
        if self.state == 1:
            self.BallPosPID(ball_pos,log)
        # if self.state == 2:
            self.send_pwm_val(0)

    def stabalize(self, ball_pos, dt,log):
        # wheel_pos = self.encoder.delt_to_rad(receive_msg())
        diff_time = dt

        # using PID variables and such, calculate PWM output
        self.integrator_val += self.e_prev * diff_time
        diff_pos = ball_pos
        pwm_kp = self.k_p * diff_pos
        pwm_kd = self.k_d * (diff_pos - self.e_prev) / diff_time
        pwm_est = (pwm_kp + pwm_kd)/5
        self.e_prev = diff_pos

        self.send_pwm_val(pwm_est)  
        if log:
            self.logger.log_data(
                0,
                diff_time,
                curr_pos,
                diff_pos,
                set_pos,
                0,
                pwm_kp,
                0,
                pwm_kd,
                ball_pos,
            )
        # if (round(derivative,5) == 0)l and (abs(ball_pos) < 10): # TODO check
        #     self.state += 1
        #     time.sleep(1)
        #     print("stabalized")

    def BallPosPID(self, curr_pos,log):
        # get encoder value from UART
        print("in ball")
        curr_time = time.time()
        diff_time = curr_time - self.start_time
        self.start_time = curr_time
        delt_enc = receive_msg()
        diff_pos = 0 - curr_pos  # set_rpm - curr_rpm

        # using PID variables and such, calculate PWM output
        self.integrator_val += self.e_prev * diff_time

        pwm_kp = self.k_p * diff_pos
        pwm_ki = self.k_i * (self.integrator_val)
        pwm_kd = self.k_d * (diff_pos - self.e_prev) / diff_time
        pwm_est = pwm_kp + pwm_ki + pwm_kd
        self.e_prev = diff_pos
        print(pwm_est)
        self.send_pwm_val(pwm_est)
        if log:
            self.logger.log_data(
                delt_enc,
                diff_time,
                curr_pos,
                diff_pos,
                0,
                curr_time,
                pwm_kp,
                pwm_ki,
                pwm_kd,
                curr_pos,
            )

    def WheelPosPID(self, set_pos, ball_pos, log):
        k_p = 225
        k_i = 0
        k_d = 0
        if (set_pos > np.pi*2):
            print("over 2 pi input")
        # get encoder value from UART
        curr_time = time.time()
        diff_time = curr_time - self.start_time
        self.start_time = curr_time
        delt_enc = receive_msg()
        curr_pos = self.encoder.delt_to_rad(delt_enc)
        print(curr_pos)
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

        # self.send_pwm_val(pwm_est)
        if log:
            self.logger.log_data(
                delt_enc,
                diff_time,
                curr_pos,
                diff_pos,
                set_pos,
                curr_time,
                pwm_kp,
                pwm_ki,
                pwm_kd,
                ball_pos,
            )

    def exit(self, log):
        msg = str(0).ljust(7, "\t")
        send_msg(msg)
        if log:
            print("trying to write")
            self.logger.write_file()
