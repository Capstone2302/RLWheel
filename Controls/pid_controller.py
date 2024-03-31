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
        self.k_p = 2.5  # 2.25  # 4.5
        self.k_i = 13  # 1.5
        self.k_d = 0.225  # 0.5  # 2.8
        self.k_w = 0  # -2.9
        self.integrator_val = 0
        self.start_time = time.time()
        self.e_prev = 0
        self.logger = DataLogger()
        self.encoder = EncoderProcesser()
        self.r = None  # TODO
        self.state = 0

    def init_position(self):
        self.encoder.set_center_pos()
        print(self.encoder.curr_pos_rad)

    def control_routine(self, ball_pos, log):
        current_time = time.time()
        dt = current_time - self.start_time
        self.start_time = current_time

        self.prev_time = current_time
        if self.state == 0:
            self.stabalize(ball_pos, dt)
        if self.state == 1:
            self.tilt(ball_pos)
        if self.state == 2:
            self.PID_mode(ball_pos, dt)

    def stabalize(self, ball_pos, dt):
        derivative = (ball_pos - self.e_prev) / dt
        self.e_prev = ball_pos
        proportional = np.pi/2 * ball_pos
        print("prop: ", proportional)
        print("ballpos: ", ball_pos)
        wheel_pos = self.encoder.delt_to_rad(receive_msg())
        pwm_est = proportional + wheel_pos

        msg = str(int(pwm_est)).ljust(7, "\t")
        send_msg(msg)

        if (round(derivative,5) == 0) and (abs(ball_pos) < 10): # TODO check
            self.state += 1
            time.sleep(1)
            print("stabalized")

    def tilt(self, ball_pos):
        msg = str(int(30)).ljust(7, "\t")
        send_msg(msg)
        print("tilt")
        if ball_pos > 80:
            self.state += 1
            # time.sleep(1000)
    def PID_mode(self, ball_pos, dt):

        # get encoder value from UART
        diff_wheel_pos = self.encoder.delt_to_rad(receive_msg())

        diff_pos = 0 - ball_pos  # set_rpm - curr_rpm

        # using PID variables and such, calculate PWM output
        self.integrator_val += self.e_prev * dt

        pwm_kp = self.k_p * diff_pos
        pwm_ki = self.k_i * (self.integrator_val)
        pwm_kd = self.k_d * (diff_pos - self.e_prev) / dt
        pwm_est = pwm_kp + pwm_ki + pwm_kd
        self.e_prev = diff_pos

        msg = str(int(-pwm_est)).ljust(7, "\t")
        send_msg(msg)

    def PWM_Response_test(self, pwm_val, log):
        # get encoder value from UART
        delt_enc = receive_msg()
        curr_time = time.time()
        diff_time = curr_time - self.start_time
        self.start_time = curr_time

        curr_rpm = (delt_enc * 60) / (diff_time * 2400)  # CCW is positive
        # send messages over UART
        msg = str(int(pwm_val)).ljust(7, "\t")
        send_msg(msg)
        print(curr_rpm)
        if log:
            self.logger.log_data(
                delt_enc,
                diff_time,
                curr_rpm,
                0,
                curr_time,
                pwm_val,
                0,
                0,
                0,
            )

    def PID_response_test1(self, max, log_perhaps):
        # continuous tests
        for i in range(max, -max, 1):
            self.control_routine(i / 10, log_perhaps)

        for i in range(-max, max, 1):
            self.control_routine(i / 10, log_perhaps)

    def PID_response_test2(self, max, square_len, log_perhaps):
        # step response tests
        for i in range(max * 6):
            if i % square_len < square_len / 2:
                self.control_routine(max, log_perhaps)
            else:
                self.control_routine(-max, log_perhaps)

    def exit(self, log):
        msg = str(0).ljust(7, "\t")
        send_msg(msg)
        if log:
            self.logger.write_file()
