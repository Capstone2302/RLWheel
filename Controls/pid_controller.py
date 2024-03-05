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


class MotorController:  # add class definitions
    def __init__(self):
        self.k_p = 4
        self.k_i = 0.5
        self.k_d = 0
        self.integrator_val = 0
        self.start_time = time.time()
        self.e_prev = 0
        self.logger = DataLogger()

    def control_routine(self, ser, set_rpm, log):
        # get encoder value from UART
        delt_enc = receive_msg(ser)
        # get 'real' time
        curr_time = time.time()
        diff_time = curr_time - self.start_time
        self.start_time = curr_time

        # get error from set point and curr_rpm
        curr_rpm = (delt_enc * 60) / (diff_time * 2400)  # CCW is positive

        diff_rpm = 0 - set_rpm

        # using PID variables and such, calculate PWM output
        self.integrator_val = self.integrator_val + self.e_prev * diff_time

        PWM_est = (
            self.k_p * diff_rpm
            + self.k_i * (self.integrator_val + diff_rpm)
            + self.k_d * (diff_rpm - self.e_prev)
        )
        self.e_prev = diff_rpm
        # print( delt_enc, set_rpm)
        msg = str(int(PWM_est)).ljust(7, "\t")
        send_msg(ser, msg)
        if log:
            self.logger.log_data(
                delt_enc, diff_time, curr_rpm, diff_rpm, set_rpm, curr_time, PWM_est
            )

    def pwm_test_routine(self, ser, set_pwm, log):
        # get encoder value from UART
        delt_enc = receive_msg(ser)
        # get 'real' time
        curr_time = time.time()
        diff_time = curr_time - self.start_time
        self.start_time = curr_time

        # get error from set point and curr_rpm
        curr_rpm = (delt_enc * 60) / (diff_time * 2400)  # CCW is positive
        print(curr_rpm, delt_enc, set_pwm)
        # send message over UART
        msg = str(int(set_pwm)).ljust(7, "\t")
        send_msg(ser, msg)
        if log:
            self.logger.log_data(
                delt_enc, diff_time, curr_rpm, -1, -1, curr_time, set_pwm
            )

    def PID_response_test1(self, ser, max, log_perhaps):
        # continuous tests
        for i in range(max, -max, 1):
            self.control_routine(ser, i / 10, log_perhaps)

        for i in range(-max, max, 1):
            self.control_routine(ser, i / 10, log_perhaps)

    def PID_response_test2(self, ser, max, square_len, log_perhaps):
        # step response tests
        for i in range(max * 6):
            if i % square_len < square_len / 2:
                self.control_routine(ser, max, log_perhaps)
            else:
                self.control_routine(ser, -max, log_perhaps)

    def exit(self, ser, log):
        msg = str(0).ljust(7, "\t")
        send_msg(ser, msg)
        ser.close()
        if log:
            self.logger.write_file()
