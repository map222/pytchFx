# -*- coding: utf-8 -*-
"""
Created on Sat Jan 10 10:22:19 2015

@author: Me
"""

import pandas as pd
import sqlite3

def load_pitches(year, row_limit = 1000000 ):
    # open connection to sqlite database
    filename = 'pitchFX_' + str(year) + '.sqlite3'
    db = sqlite3.connect("pitchFx_2013.sqlite3")
    
    # load the pitches in
    pitches_out = pd.read_sql('SELECT * FROM pitch LIMIT' + str(row_limit), db)
    
    # fix the datatype of the break from text to int
    pitches_out['break_angle'] = pitches_out['break_angle'].astype(float)
    pitches_out['break_y'] = pitches_out['break_y'].astype(float)
    pitches_out['break_length'] = pitches_out['break_length'].astype(float)