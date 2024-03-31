"""
control_tests.py

Description:
Seperation for PID Tests and abstraction

Usage:
- Test the PID for internal motor tuning

Author:
Ashli Forbes

Date:
Created - 30/03/20234
"""

from .pid_controller import MotorController
import time
import numpy as np
from scipy import signal


class TestClass:
    def __init__(self):
        self.cont = MotorController()

    def PWM_Response_test(self, pwm_val, log):
        # get encoder value from UARTr
        delt_enc = self.cont.receive_delt_enc()
        curr_time = time.time()
        diff_time = curr_time - self.start_time
        self.start_time = curr_time

        curr_rpm = (delt_enc * 60) / (diff_time * 2400)  # CCW is positive
        # send messages over UART
        self.cont.send_pwm_val(pwm_val)
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

    def Wheel_PID_Test_Gradient(self, max, log_perhaps):
        # continuous tests
        max = max * 100
        for i in range(max, 0, -1):
            self.cont.WheelPosPID(i / 100, log_perhaps)
            print(i / 100)
        for i in range(0, max, 1):
            self.cont.WheelPosPID(i / 100, log_perhaps)

    def Wheel_PID_Test_Square(self, max, square_len, log_perhaps):
        # step response tests
        t = np.linspace(0, 1, 500, endpoint=False)
        step = signal.square(2 * np.pi *2* t)
        step = step * max / 2 + max 
        for i in step:
            print(i)
            self.cont.WheelPosPID(i, log_perhaps)
