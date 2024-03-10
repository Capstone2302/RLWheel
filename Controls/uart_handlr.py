"""
uart_handlr.py 

Handle the UART portion of the control loop

Author:
Ashli Forbes

Date:
Created - 26/11/2023
"""
import serial

def send_msg(ser, command):
    ser = serial.Serial("/dev/ttyUSB0", baudrate=115200, stopbits=1, timeout=100)
    ser.write(command.encode())
    ser.close


def receive_msg(ser):

    ser = serial.Serial("/dev/ttyUSB0", baudrate=115200, stopbits=1, timeout=100)
    line = ser.readline(12).decode().strip()
    ser.close()
    # if len(line) < 5:
    #     return -1
    print(line)
    # line = list(line)
    # val = 0
    # negative = False
    # for i in range(0, len(line)):
    #     if line[i] == "\x00":
    #         continue
    #     elif line[i] == "-":
    #         negative = True
    #     else:
    #         val = val * 10 + float(line[i])
    # if negative:
    #     return val * -1
    return int(line)
