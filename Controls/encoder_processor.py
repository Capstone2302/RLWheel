"""
encoder_processor.py 

Pre process the encoder data for sim2real application

Author:
Ashli Forbes

Date:
Created - 28/03/2024
"""
import numpy as np

class EncoderProcesser:

    def __init__(self):
        self.ticks_per_rev = 2400/4
        self.orientation = "clockwise"
        self.curr_pos_ticks = 0
        self.curr_pos_rad = 0
    
    def delt_to_rad(self,delt_enc):
        self.curr_pos_ticks+= delt_enc
        scale = 2*np.pi/(self.ticks_per_rev)
        
        if self.curr_pos_ticks >= self.ticks_per_rev:
            self.curr_pos_ticks-= self.ticks_per_rev
            return self.curr_pos_rad         
        elif self.curr_pos_ticks < 0:
            self.curr_pos_ticks += self.ticks_per_rev

        self.curr_pos_rad = self.curr_pos_ticks*scale
        return self.curr_pos_rad
    
    def set_center_pos(self):
        self.curr_pos_ticks = 0
        self.curr_pos_rad = 0