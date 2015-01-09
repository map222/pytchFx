# -*- coding: utf-8 -*-
"""
Created on Thu Jan 08 20:45:46 2015

@author: Me
"""
import pdb

def get_pitches_from_template(tp, ap, sp_var = 1,
    px_var = 0.1, pz_var = 0.1, br_angle = 10 ):
    """
    tp = template pitch, ap = all_pitches
    sp_var = speed, px/pz = location over plate, br_angle = break
    """
    
    pdb.set_trace()
    
    # convert all the values into scalars for input into query
    tp_end_speed = float(tp.end_speed) 
    
    new_pitches = ap[ (ap['end_speed'] > tp_end_speed - sp_var) & (ap['end_speed'] < tp_end_speed + sp_var) ]
    return new_pitches