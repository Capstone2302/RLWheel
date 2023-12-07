"""
pid_controller.py 

Description:
Class that runs and abstractsthe PID control loop of the motor

Usage:
- Is called from other aspects of the program to output the PWM 

Author:
Ashli Forbes

Date:
Created - 03/12/2023
"""
import time
from .uart_handlr import receive_msg, send_msg 


class MotorController:
    def __init__(self):
        self.k_p = 4
        self.k_i = 0
        self.k_d = 0
        self.integrator_val = 0 
        self.start_time = time.time()
        self.e_prev = 0
        

    def control_routine(self,ser, set_rpm):
            # get encoder value from UART
            delt_enc = receive_msg(ser)
            # get 'real' time    
            curr_time = time.time()
            diff_time = curr_time - self.start_time
            self.start_time = curr_time
            # get error from set point and real
            curr_rpm = (delt_enc)*60/(diff_time*2400)  #it seems that CCW is positive
            
            diff_rpm = float(set_rpm) # - curr_rpm 
            # set_rpm = curr_rpm

            # using PID variables and such, calculate PWM output
            self.integrator_val = self.integrator_val + self.e_prev*diff_time

            PWM_est = self.k_p*diff_rpm + self.k_i*(self.integrator_val  + diff_rpm) + self.k_d*(diff_rpm - self.e_prev)
            self.e_prev = diff_rpm

            # send message over UART
            print(PWM_est, delt_enc)
            msg = str(int(PWM_est)).ljust(7, '\t')
            send_msg(ser, msg)