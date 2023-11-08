import serial

# Define the serial port and its settings
ser = serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=1) 

try:
    while True:
        # Read data from the UART
        data = ser.readline()
        print(data, end='')  # Print the received data
        
except KeyboardInterrupt:
    # Handle Ctrl+C to exit the program gracefully
    print("Exiting...")

finally:
    ser.close()  # Close the serial connection when done


