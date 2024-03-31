"""
data_logger.py

Description:
Datalogger

Usage:
- Log data from ball detection and motor controller

Author:
Ashli Forbes

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
        self.set_point = []
        self.loop_time = []
        self.curr_set = []
        self.diff_set = []
        self.pwm_kp = []
        self.pwm_ki = []
        self.pwm_kd = []
        self.pwm_kw = []
        self.curr_time = []

    def log_data(
        self,
        delt_enc,
        loop_time,
        curr_set,
        diff_set,
        set_point,
        curr_time,
        pwm_kp,
        pwm_ki,
        pwm_kd,
        pwm_kw,
    ):
        self.delt_enc.append(delt_enc)
        self.loop_time.append(loop_time)
        self.curr_set.append(curr_set)
        self.diff_set.append(diff_set)
        self.set_point.append(set_point)
        self.curr_time.append(curr_time)
        self.pwm_kp.append(pwm_kp)
        self.pwm_ki.append(pwm_ki)
        self.pwm_kd.append(pwm_kd)
        self.pwm_kw.append(pwm_kw)

    def write_file(self):
        data = {
            "DeltEncoder": self.delt_enc,
            "LoopTimes": self.loop_time,
            "CurrRpm": self.curr_set,
            "DiffSet": self.diff_set,
            "SetPoint": self.set_point,
            "CurrTime": self.curr_time,
            "KpContrib": self.pwm_kp,
            "KiContrib": self.pwm_ki,
            "KdContrib": self.pwm_kd,
            "KwContrib": self.pwm_kw,
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
