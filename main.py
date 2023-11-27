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

# Define the serial port and its settings
ser = serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=200) 

start_time = time.time()
start_rpm = 300 # this is a dummy variable for now
e_prev = 1 # another temp variable

def send_command(command):
    print(command.encode())
    ser.write(command.encode())

def main():
    """
    The main entry point of the application.

    More detailed information about what the main function does goes here,
    explaining its purpose and overall program flow.

    """
    # Your main program logic goes here

    k_p = 0.05
    k_i = 0.001
    k_d = 0.00001

    i = 0 
    
    try:
        while True:
            # get set speed from user (in RPM)
            user_input = input("Enter command (1 for ON, 0 for OFF, q to quit): ")+ '\n'

            # get encoder value from UART
            line = ser.readline().decode('utf-8').strip()

            # get 'real' time 
            curr_time = time.time()
            diff_time = start_time - curr_time
            start_time = curr_time

            # calculate current rpm 
            curr_rpm = line*60/diff_time

            # get error from set point and real
            diff_rpm = start_rpm - curr_rpm
            start_rpm = curr_rpm

            # using PID variables and such, calculate PWM output

            PWM_est = k_p*diff_rpm + k_i*(i + diff_rpm) + k_d*(diff_rpm - e_prev)
            e_prev = diff_rpm

            # send PWM over UART
            PWM_est = PWM_est.ljust(7, '\t')
            print(curr_prm)
            send_command(PWM_est)

    except KeyboardInterrupt:
        # Handle Ctrl+C to exit gracefully
        print("\nScript terminated by user.")

    finally:
        # Close the serial port
        ser.close()


    

if __name__ == "__main__":
    main()