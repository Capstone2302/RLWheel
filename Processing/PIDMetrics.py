import numpy as np 
import pandas as pd 
import csv
import matplotlib.pyplot as plt

from pathlib import Path 

filepath = Path("Processing/Logs/2023-12-03_15-12-47.csv")  

columns = ["SetRpm","PWMEst", "CurrRpm", "DeltRpm"]
df = pd.read_csv(filepath, usecols = columns) 
# Set a threshold for the maximum allowed jump
max_jump = 1000

# Identify rows where the jump is too large
large_jump_indices = df['PWMEst'].diff().abs() > max_jump
# large_jump_indices = df['PWMEst'].diff().abs() > max_jump

# Remove or modify the rows with large jumps
df_filtered = df[~large_jump_indices].copy()

df_filtered.plot(title = "DataFrame Plot")
plt.show()