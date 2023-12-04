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
import pandas as pd 
from pathlib import Path 
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
    k_p = 0.4
    k_i = 1
    k_d = 0.1
    i = 0 
    start_time = time.time()
    set_rpm = 230 # this is a dummy variable for now
    e_prev = 0 # another temp variable
    date_time = (time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(start_time)))
    print(date_time)
    setup ={"Kp":[k_p],
            "Ki": [k_i],
            "IntegratorValue":[i],
            "Kd": [k_d],
            "StartTime": [start_time],
            }
    
    filepath = Path("Processing/Setup/" + date_time + ".csv")  
    filepath.parent.mkdir(parents=True, exist_ok=True)
    df_setup = pd.DataFrame(setup)  
    df_setup.to_csv(filepath)
    dynamic_dict = {
            "DeltEncVal": [],
            "CurrTime":[],
            "DeltTime": [],
            "CurrRpm": [],
            "DeltRpm": [],
            "SetRpm":[],
            "PWMEst":[],
            }

    try:
        while True:
        # for i in range(-300,300, 10):

            # get encoder value from UART
            delt_enc = receive_msg(ser)

            # get 'real' time    
            curr_time = time.time()
            diff_time = curr_time - start_time
            start_time = curr_time
            # calculate rpm
            # delt_enc = enc_val - env_prev 
            # if (abs(delt_enc > 4000) or env_prev == 0):
            #     env_prev = enc_val
            #     continue
            curr_rpm = (delt_enc)*60/(diff_time*2400)  #it seems that CCW is positive
            
            # get error from set point and real
            diff_rpm = float(set_rpm) - curr_rpm 
            # set_rpm = curr_rpm

            # using PID variables and such, calculate PWM output
            i = i + e_prev*diff_time

            PWM_est = k_p*diff_rpm + k_i*(i + diff_rpm) + k_d*(diff_rpm - e_prev)
            e_prev = diff_rpm

            # send PWM over UART
            # if (PWM_est < 0):
            #     PWM_est = 10
            
            msg = str(int(PWM_est)).ljust(7, '\t')
            send_msg(ser, msg)
            print(int(PWM_est), curr_rpm, delt_enc)

            # send_msg(ser, msg)
            # dynamic_dict["CurrTime"].append(curr_time)
            # dynamic_dict["DeltTime"].append(diff_time)
            # dynamic_dict["SetRpm"].append(set_rpm)
            # dynamic_dict["DeltEncVal"].append(delt_enc)
            # dynamic_dict["CurrRpm"].append(curr_rpm)
            # dynamic_dict["DeltRpm"].append(diff_rpm)
            # dynamic_dict["PWMEst"].append(PWM_est)

    except KeyboardInterrupt:
        # Handle Ctrl+C to exit gracefully
        print("\nScript terminated by user.")


    finally:  
        # filepath = Path("Processing/Logs/" + date_time + ".csv")  
        # filepath.parent.mkdir(parents=True, exist_ok=True)  
        # df = pd.DataFrame(dynamic_dict)
        # df.to_csv(filepath)
        msg = str(0).ljust(7, '\t')
        send_msg(ser, msg)
        # df = pd.DataFrame(dynamic_dict)
        # df.to_csv("log.csv")
        # Close the serial port
        ser.close()


    

if __name__ == "__main__":
    main()