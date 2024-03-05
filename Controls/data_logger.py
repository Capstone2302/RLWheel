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
        self.date_time = time.strftime(
            "%Y-%m-%d_%H-%M-%S", time.localtime(self.start_time)
        )
        self.filepath = Path("Processing/Logs/" + self.date_time + ".csv")
        self.delt_enc = []
        self.set_rpm = []
        self.loop_time = []
        self.curr_rpm = []
        self.pwm_req = []
        self.delt_rpm = []
        self.pid_vals = []
        self.curr_time = []

    def log_data(
        self, delt_enc, loop_time, curr_rpm, delt_rpm, set_rpm, curr_time, pwm_req
    ):
        self.delt_enc.append(delt_enc)
        self.loop_time.append(loop_time)
        self.curr_rpm.append(curr_rpm)
        self.delt_rpm.append(delt_rpm)
        self.set_rpm.append(set_rpm)
        self.curr_time.append(curr_time)
        self.pwm_req.append(pwm_req)

    def write_file(self):
        data = {
            "DeltEncoder": self.delt_enc,
            "LoopTimes": self.loop_time,
            "CurrRpm": self.curr_rpm,
            "ChangeInRpm": self.delt_rpm,
            "SetRpm": self.set_rpm,
            "CurrTime": self.curr_time,
            "PWMReq": self.pwm_req,
        }
        df = pd.DataFrame(data)
        df.to_csv(self.filepath)


class DataLogger_Ball:
    def __init__(self):
        self.start_time = time.time()
        self.date_time = time.strftime(
            "%Y-%m-%d_%H-%M-%S", time.localtime(self.start_time)
        )
        self.filepath = Path("Processing/Ball/" + self.date_time + ".csv")
        self.pos_err = []
        self.loop_time = []
        self.curr_time = []

    def log_data(self, pos_err, loop_time, curr_time):
        self.pos_err.append(pos_err)
        self.loop_time.append(loop_time)  # TODO: take an average of loop times
        self.curr_time.append(curr_time)

    def write_file(self):
        data = {
            "PositionErr": self.pos_err,
            "LoopTimes": self.loop_time,
            "CurrTime": self.curr_time,
        }
        df = pd.DataFrame(data)
        df.to_csv(self.filepath)
