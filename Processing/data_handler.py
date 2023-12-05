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

class DataProcessor: 
    def __init__(self):
        log_files = glob.glob("Processing/Logs/*.csv")  
        log_files.sort(key=os.path.getmtime, reverse=True)
        self.log_files_list = log_files

    def get_log_files_list(self):
        return self.log_files_list

    def get_last_log(self):
        if self.log_files_list:
            return self.log_files_list[0]
        else:
            return None #TODO: raise a proper exception
        
    def get_headers(self):
        pass

    def get_frame_from_header(self):
        pass
    