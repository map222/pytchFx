# -*- coding: utf-8 -*-
"""
Created on Thu Jan 08 20:45:46 2015

@author: Michael Patterson
"""
import pdb
import pandas as pd
import numpy as np



# return all pitches similar to a given single template
def get_pitches_from_template(tp, ap, sp_var = 1, px_var = 0.15, pz_var = 0.15,
                              x0_var = 0.5, z0_var = 0.5, br_angle_var = 10 ):
    """
    tp = template pitch (dataframe.loc[index])
    ap = all_pitches
    sp_var = speed, px/pz = location over plate, br_angle = break
    """
    
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
    
    resampled_pitches = [] # a list of dataframes with resampled data
    
    # go through all template pitches, and add new data (need append because can be multiple pitches)
    for i, row in template_pitches.iterrows():
        resampled_pitches.append(get_pitches_from_template(row, all_pitches))
    
    return pd.concat(resampled_pitches) # concatenate all the dataframes into one
    
def calc_results_from_pitches(pitch_abs):
    """ calculates results from a pitch_ab dataframe
        first it counts numbers of balls, strikes, etc
        then normalizes per pitch """

    # count the number of results for each pitch
    des_results = pitch_abs.groupby('des').size() / len(pitch_abs)
    balls = des_results[['Ball', 'Ball In Dirt', 'Intent Ball', 'Pitchout']].sum()
    fouls = des_results[['Foul', 'Foul (Runner Going)', 'Foul Tip', 'Foul Bunt']].sum()
    swing_strikes = des_results[['Swinging Strike', 'Missed Bunt', 'Swinging Strike (Blocked)']].sum()
    in_play = des_results[['In play, no out', 'In play, out(s)', 'In play, run(s)']].sum()
    
    kept_results = des_results[['Called Strike', 'Hit By Pitch']]
        
    return kept_results.append(pd.Series([balls, fouls, swing_strikes, in_play], ['Ball', 'Foul', 'Swinging Strike', 'In Play']))
            
def merge_pitch_ab(pitches_in, abs_in):
    """ merge a pitch and atbat dataframe """
    # create merged db with just information about pitch, and results it got    
    return pd.merge(pitches_in, abs_in, how = 'inner', on=['num', 'gameday_link'])

def calc_runs_all_pitches(pitch_abs):
    """ Calculate the expected runs per pitch; need pitch_ab dataframe to get results of hits """
    pitch_abs['exp_val'] = pitch_abs.apply(calc_runs_per_pitch, axis = 1)    
    
    return pitch_abs

    #counts =                [0-0,   0-1,   0-2,   1-0,  1-1,   1-2,   2-0,   2-1, 2-2, 3-0, 3-1, 3-2]
    ball_value = np.array(   [0.034, 0.029, 0.022, 0.05, 0.045, 0.035, 0.099, 0.09, 0.085, 0.112, 0.17, 0.243])
    strike_value = -1 * np.array([0.038, 0.051, 0.155, 0.043, 0.058, 0.178, 0.049, 0.067, 0.213, 0.058, 0.073, 0.298])
    count_distrib = np.array([0.26, 0.13, 0.06, 0.1, 0.1, 0.093, 0.036, 0.053, 0.079, 0.012, 0.022, 0.047])
    val_ball = np.sum(ball_value * count_distrib)
    val_strike = np.sum(strike_value * count_distrib)
    
    true_dict = {}
    true_dict.update(dict.fromkeys(['Ball', 'Ball In Dirt', 'Intent Ball', 'Pitchout'], val_ball))
    true_dict.update(dict.fromkeys(['Foul', 'Foul (Runner Going)', 'Foul Tip', 'Foul Bunt',
                                     'Called Strike', 'Swinging Strike', 'Missed Bunt',
                                     'Swinging Strike (Blocked)'], val_strike))
    true_dict.update(dict.fromkeys(['In play, no out', 'In play, out(s)', 'In play, run(s)'], np.nan ))
    true_dict.update(dict.fromkeys(['Hit By Pitch'], 0.33))
    
    hit_dict = { }
    hit_dict.update(dict.fromkeys(['Groundout', 'Flyout', 'Lineout', 'Grounded Into DP',
                                   'Bunt Groundout', 'Pop Out', 'Field Error', 'Sac Fly', 'Sac Bunt',
                                   'Forceout'], -0.27))
    hit_dict.update(dict.fromkeys(['Single'], 0.47))
    hit_dict.update(dict.fromkeys(['Double'], 0.75))
    hit_dict.update(dict.fromkeys(['Triple'], 1.04))
    hit_dict.update(dict.fromkeys(['Home Run'], 1.4))

def calc_runs_per_pitch(pitch_ab):
    """ Function called by calc_runs_per_pitch and applied to each row """

    
    value_out = true_dict[pitch_ab['des']]

    # if the value_out is NaN, it means the ball was in play    
    if np.isnan(value_out):
        value_out = hit_dict[pitch_ab['event']]
    
    return value_out