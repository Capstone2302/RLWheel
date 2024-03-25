"""
uart_handlr.py 

Handle the UART portion of the control loop

Author:
Ashli Forbes

Date:
Created - 26/11/2023
"""
import serial

last =0 
def send_msg(command):  # TODO allow for general usb ports
    ser = serial.Serial("/dev/ttyUSB0", baudrate=115200, stopbits=1, timeout=100)
    ser.write(command.encode())
    ser.close


def receive_msg():
    ser = serial.Serial("/dev/ttyUSB0", baudrate=115200, stopbits=1, timeout=100)
    line = ser.readline().decode()
    # if len(line)<3:
    #     print(repr(line))
    #     return -10000
    line = line.strip('\x00')
    ser.close()
    return 0
