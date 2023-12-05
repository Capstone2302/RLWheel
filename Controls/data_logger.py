"""
data_logger.py

Description:
Datalogger

Usage:
-

Date:
Created - 04/12/2023
"""

import time
from pathlib import Path 
import pandas as pd
class DataLogger:
    def __init__(self):
        self.start_time = time.time()
        self.date_time = (time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(self.start_time)))
        self.filepath = Path("Processing/Logs/" + self.date_time + ".csv")  
        self.delt_enc = []
        self.loop_time = []
        self.curr_rpm = []
        self.delt_rpm = []
        self.pid_vals = []
        

    def create_file(self):
        pass

    def log_data(self, delt_enc, loop_time, curr_rpm, delt_rpm):
        self.delt_enc.insert(0,delt_enc)
        self.loop_time.insert(0,loop_time) #TODO: take an average of loop times
        self.curr_rpm.insert(0,curr_rpm)
        self.delt_rpm.insert(0,delt_rpm)

    def write_file(self):
        data = {"DeltEncoder": self.delt_enc,
                "LoopTimess": self.loop_time,
                "CurrRpm": self.curr_rpm,
                "ChangeInRpm":self.delt_rpm}
        df = pd.DataFrame(data)
        df.to_csv(self.filepath)
