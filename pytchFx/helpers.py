# -*- coding: utf-8 -*-
"""
Created on Thu Jan 08 20:45:46 2015

@author: Michael Patterson
"""
import pdb

def get_pitches_from_template(tp, ap, sp_var = 1, px_var = 0.15, pz_var = 0.15,
                              x0_var = 0.5, z0_var = 0.5, br_angle_var = 10 ):
    """
    tp = template pitch, ap = all_pitches
    sp_var = speed, px/pz = location over plate, br_angle = break
    """
    
    
    # convert all the values into scalars for input into query
    tp_end_speed = float(tp.end_speed) 
    tp_px = float(tp.px)
    tp_pz = float(tp.pz)
    tp_x0 = float(tp.x0)
    tp_z0 = float(tp.z0)
    tp_br = float(tp.break_angle)
    
   # pdb.set_trace()
    
    new_pitches = ap[ (ap['end_speed'] > tp_end_speed - sp_var) & (ap['end_speed'] < tp_end_speed + sp_var) 
       & (ap['px'] > tp_px - px_var) & (ap['px'] < tp_px + px_var) 
       & (ap['pz'] > tp_pz - pz_var)  & (ap['pz'] < tp_pz + pz_var) 
       & (ap['x0'] > tp_x0 - x0_var) & (ap['x0'] < tp_x0 + x0_var) 
       & (ap['z0'] > tp_z0 - z0_var) & (ap['z0'] < tp_z0 + z0_var) 
       & (ap['break_angle'] > tp_br - br_angle_var) & (ap['break_angle'] < tp_br + br_angle_var) ]
    return new_pitches