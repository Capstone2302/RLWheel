import serial

# Define the serial port and its settings
ser = serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=200) 


def send_command(command):
    print(command.encode())
    ser.write(command.encode())


try:
    while True:
        # Poll for user input
        user_input = input("Enter command (1 for ON, 0 for OFF, q to quit): ")+ '\n'

        # Check if the user wants to quit
        if user_input.lower() == 'q':
            break

        # Send the command to the Bluepill
        user_input = user_input.ljust(7, '\t')
        send_command(user_input)

except KeyboardInterrupt:
    # Handle Ctrl+C to exit gracefully
    print("\nScript terminated by user.")

finally:
    # Close the serial port
    ser.close()