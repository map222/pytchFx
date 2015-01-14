# -*- coding: utf-8 -*-
"""
Created on Thu Jan 08 20:45:46 2015

@author: Michael Patterson
"""
import pdb
import pandas as pd

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
    
    # do I want to do merge outside this?
def calc_results_from_pitches(sample_pitches, pitch_abs):
    """ calculates the balls, strikes, ..., from a sample data frame containing one or more pitches """
    
    pitch_info = ['px', 'pz', 'x0', 'z0', 'break_angle', 'end_speed']
    results_info = ['num', 'gameday_link', 'des', 'event']

    # get the pitches of the sample pitches
    sim_pitches = pd.DataFrame(columns = pitch_abs.columns.values.tolist())
    
    pdb.set_trace()
    for i, rows in sample_pitches.iterrows():
        sim_pitches = sim_pitches.append(get_pitches_from_template(rows, pitch_abs))
        
    # count the number of results for each pitch
    sample_results = sample_pitches.groupby('des').size() / len(sample_pitches)
    sim_pitches = sim_pitches.groupby('des').size() / len(sim_pitches)
    
#def get_subset_pitches(pitch_abs_in):
    
def calc_results_pitches(pitch_abs_in):
    
            
def merge_pitch_ab(pitches_in, abs_in):
    """ merge a pitch and atbat dataframe """
    # create merged db with just information about pitch, and results it got    
    return pd.merge(pitches_in, abs_in, how = 'inner', on=['num', 'gameday_link'])
    