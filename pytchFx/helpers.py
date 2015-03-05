# -*- coding: utf-8 -*-
"""
Created on Thu Jan 08 20:45:46 2015

@author: Michael Patterson
"""
import pdb
import pandas as pd

# return all pitches similar to a given single template
def get_pitches_from_template(tp, ap, sp_var = 1, px_var = 0.15, pz_var = 0.15,
                              x0_var = 0.5, z0_var = 0.5, br_angle_var = 10 ):
    """
    tp = template pitch (dataframe.loc[index])
    ap = all_pitches
    sp_var = speed, px/pz = location over plate, br_angle = break
    """
    
    #pdb.set_trace()
    # convert all the values into scalars for input into query
    tp_end_speed = float(tp.end_speed) 
    tp_px = float(tp.px)
    tp_pz = float(tp.pz)
    tp_x0 = float(tp.x0)
    tp_z0 = float(tp.z0)
    tp_br = float(tp.break_angle)
    
    end_str = '(end_speed > @tp_end_speed - @sp_var) & (end_speed < @tp_end_speed + @sp_var) & '
    px_str = '(px > @tp_px - @px_var) & (px < @tp_px + @px_var) & '
    pz_str = '(pz > @tp_pz - @pz_var) & (pz < @tp_pz + @pz_var) & '
    x0_str = '(x0 > @tp_x0 - @x0_var) & (x0 < @tp_x0 + @x0_var) & '
    z0_str = '(z0 > @tp_z0 - @z0_var) & (z0 < @tp_z0 + @z0_var) & '
    break_str = '(break_angle > @tp_br - @br_angle_var) & (break_angle < @tp_br + @br_angle_var)'
    
    new_pitches = ap.query(end_str + px_str + pz_str + x0_str + z0_str + break_str)
    
    return new_pitches

def get_pitches_from_templates(template_pitches, all_pitches):
    """ return all pitches, given a bunch of template pitches
        calls get_pitches_from_template function for each pitch times)
        template_pitches: dataframe[indices] (NOT dataframe.loc[indices])
        all_pitches: full dataframe """
    # create empty dataframe
    resampled_pitches = pd.DataFrame(columns = all_pitches.columns.values.tolist())     
    
    # go through all template pitches, and add new data (need append because can be multiple pitches)
    for i, row in template_pitches.iterrows():
        resampled_pitches = resampled_pitches.append(get_pitches_from_template(row, all_pitches))
    # the dynamic addition works fine for small samples, but as you go beyond say 200 pitches, it nonlinearly slows thing down
        # time / pitch for 100 pitches = 0.08sec
        # time / pitch for 2000 pitches = 0.27 sec
        
    return resampled_pitches
    
def calc_results_from_pitches(pitch_abs):
    """ calculates results from a pitch_ab dataframe
        first it counts numbers of balls, strikes, etc
        then normalizes per pitch """

    # count the number of results for each pitch
    des_results = pitch_abs.groupby('des').size() / len(pitch_abs)
    balls = des_results[['Ball', 'Ball In Dirt', 'Intent Ball', 'Pitchout']].sum()
    fouls = des_results[['Foul', 'Foul (Runner Going)', 'Foul Tip', 'Foul Bunt']].sum()
    swing_strikes = des_results[['Swinging Strike', 'Missed Bunt', 'Swinging Strike (Blocked)']].sum()
    #pdb.set_trace()
    kept_results = des_results[['In play, no out', 'In play, out(s)', 'In play, run(s)', 'Called Strike', 'Hit By Pitch']]
        
    return kept_results.append(pd.Series([balls, fouls, swing_strikes], ['Ball', 'Foul', 'Swinging Strike']))
    
#def get_subset_pitches(pitch_abs_in):
            
def merge_pitch_ab(pitches_in, abs_in):
    """ merge a pitch and atbat dataframe """
    # create merged db with just information about pitch, and results it got    
    return pd.merge(pitches_in, abs_in, how = 'inner', on=['num', 'gameday_link'])

# this way of cleaning results in the database is super slow
# better to just do it afterwards
def clean_results(pitch_abs):
    """ Group all of the rare events into more common descriptors """
    pitch_abs.replace('Ball In Dirt', 'Ball', inplace = True)
    pitch_abs.replace('Foul (Runner Going)', 'Foul', inplace = True)
    pitch_abs.replace('Foul Tip', 'Foul', inplace = True)
    pitch_abs.replace('Foul Bunt', 'Foul', inplace = True)
    pitch_abs.replace('Intent Ball', 'Ball', inplace = True)
    pitch_abs.replace('Pitchout', 'Ball', inplace = True)
    pitch_abs.replace('Missed Bunt', 'Swinging Strike', inplace = True)
    pitch_abs.replace('Swinging Strike (Blocked)', 'Swinging Strike', inplace = True)
    return pitch_abs