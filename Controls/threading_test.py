# import sys
# import select

# motor_command = None

# while True:
#     print("Doing something else while waiting for input...")

#     # Check if there's input available
#     ready, _, _ = select.select([sys.stdin], [], [], 0.6)

#     if ready:
#         # Read the input and update the motor_command
#         motor_command = input("Enter motor command in rpm: ") + '\n'
#         print("Received motor command:", motor_command)

#     # Continue with the rest of your code
#     # ...

#     # Check if the motor_command has been updated
#     if motor_command is not None:
#         print("Processing motor command:", motor_command)
#         # Reset motor_command after processing
#         motor_command = None


import pandas as pd 

df = pd.DataFrame({'name': ['Raphael', 'Donatello'],
                   'mask': ['red', 'purple'],
                   'weapon': ['sai', 'changeagain']})

print(df['name'])

# df.to_csv("out.csv", mode= 'a', header = False)