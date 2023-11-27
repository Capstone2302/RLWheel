"""
uart_handlr.py 

Handle the UART portion of the control loop

Author:
Ashli Forbes

Date:
Created - 26/11/2023
"""

# import serial

def send_msg(ser, command):
    ser.write(command.encode())

def receive_msg(ser):
    line = ser.readline(12).decode().strip() 
    
    if (len(line) < 4): 
        return -1 #maybe handle this a bit better

    line = list(line)
    val = line[-1]
    return val 