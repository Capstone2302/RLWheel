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
import time
import sys
import select
import csv
from Controls.uart_handlr import receive_msg, send_msg  #TODO: import properly

# Define the serial port and its settings
ser = serial.Serial('/dev/ttyUSB0', baudrate=115200, stopbits=1, timeout=100) 

def main():
    """
    The main entry point of the application.

    More detailed information about what the main function does goes here,
    explaining its purpose and overall program flow.

    """
    # Your main program logic goes here
    # TODO: Abstract this properly
    k_p = 1
    k_i = 0.005
    k_d = 0.00001

    i = 0 
    start_time = time.time()
    set_rpm = 30 # this is a dummy variable for now
    e_prev = 1 # another temp variable
    env_prev = 1000
    f = open("logfile.txt", "a")
    f.write(str(start_time) + "\n")
    f.write("Set_RPM,Current_RPM,PWM_Estimate,Encoder_Val" + "\n")
    try:
        while True:
            # get set speed from user (in RPM)
            # ready, _, _ = select.select([sys.stdin], [], [], 0.6)
            # if ready:
            #     # Read the input and update the motor_command
            #     set_rpm = input("Enter motor command in rpm: ")
            #     # set_rpm = float(set_rpm)
            #     #print("Received motor command:", set_rpm)

            # get encoder value from UART
            enc_val = receive_msg(ser)
            if(enc_val == -1):
                continue

            # get 'real' time    
            curr_time = time.time()
            diff_time = curr_time - start_time
            start_time = curr_time
            # calculate rpm
            curr_rpm = (enc_val-env_prev)*60/(diff_time*2400)

            # get error from set point and real
            diff_rpm = float(set_rpm) - curr_rpm
            # set_rpm = curr_rpm

            # using PID variables and such, calculate PWM output

            PWM_est = k_p*diff_rpm + k_i*(i + diff_rpm) + k_d*(diff_rpm - e_prev)
            e_prev = diff_rpm
            env_prev = enc_val

            # send PWM over UART
            msg = str(int(PWM_est)).ljust(7, '\t')
            print(int(PWM_est), diff_rpm)

            f.write(str(set_rpm) + "," + str(curr_rpm) + "," + str(PWM_est) + "," +  str(enc_val) +"\n") 

            send_msg(ser, msg)



    except KeyboardInterrupt:
        # Handle Ctrl+C to exit gracefully
        print("\nScript terminated by user.")

    finally:
        f.close()
        msg = str(0).ljust(7, '\t')
        send_msg(ser, msg)
    #     # Close the serial port
    #     ser.close()


    

if __name__ == "__main__":
    main()