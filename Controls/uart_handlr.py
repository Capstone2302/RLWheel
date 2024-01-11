"""
uart_handlr.py 

Handle the UART portion of the control loop

Author:
Ashli Forbes

Date:
Created - 26/11/2023
"""


def send_msg(ser, command):
        ser.write(command.encode())

def receive_msg(ser):
        line = ser.readline(12).decode().strip() 
        
        if (len(line) < 5): 
            return -1 

        line = list(line)
        val = 0
        negative = False
        for i in range(0,len(line)):
            if line[i] == '\x00':
                continue
            elif line[i] == '-':
                negative = True
            else:
                val = val*10 + float(line[i])
        if negative:
            return val*-1
        return val 