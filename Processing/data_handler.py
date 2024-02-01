"""
data_handler.py

Description:
Class that handles all logging portions and allows for data files to be generated

Usage:
-

Date:
Created - 04/12/2023
"""
from pathlib import Path
import os
import glob
import pandas as pd


class DataProcessor:
    def __init__(self):
        log_files = glob.glob("Processing/Logs/*.csv")
        log_files.sort(key=os.path.getctime, reverse=True)
        self.log_files_list = log_files

    def get_log_files_list(self):
        return self.log_files_list

    def get_last_log(self):
        if self.log_files_list:
            return self.log_files_list[0]
        else:
            return None  # TODO: raise a proper exception

    def get_last_frame(self):
        if self.log_files_list:
            return pd.read_csv(self.log_files_list[0])
        else:
            return None  # TODO: raise a proper exception

    def get_frame_from_csv(self, csv_filepath):
        return pd.read_csv(csv_filepath)

    def get_headers(self, df):
        return df.columns

    def get_frame_from_header(self, df, header):
        return df[header]


class DataProcessor_Ball:
    def __init__(self):
        log_files = glob.glob("Processing/Ball/*.csv")
        log_files.sort(key=os.path.getmtime, reverse=True)
        self.log_files_list = log_files

    def get_log_files_list(self):
        return self.log_files_list

    def get_last_log(self):
        if self.log_files_list:
            return self.log_files_list[0]
        else:
            return None  # TODO: raise a proper exception

    def get_last_frame(self):
        if self.log_files_list:
            return pd.read_csv(self.log_files_list[0])
        else:
            return None  # TODO: raise a proper exception

    def get_frame_from_csv(self, csv_filepath):
        return pd.read_csv(csv_filepath)

    def get_headers(self, df):
        return df.columns

    def get_frame_from_header(self, df, header):
        return df[header]
