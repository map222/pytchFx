# -*- coding: utf-8 -*-
"""
Created on Sat Jan 10 10:22:19 2015

@author: Me
"""

import pandas as pd
import sqlite3
import pdb

def load_pitches(year, row_limit = 1000000 ):
    """ Loads pitch database from sqlite file in directory
        
    year: integer  for year
    
    row_limit" is in case you want to limit how much info you get
    """
    
    pdb.set_trace()
    
    # open connection to sqlite database
    filename = 'pitchFX_' + str(year) + '.sqlite3'
    db = sqlite3.connect(filename)
    
    # load the pitches in
    pitches_out = pd.read_sql('SELECT * FROM pitch LIMIT ' + str(row_limit), db)
    
    # fix the datatype of the break from text to int
    pitches_out['break_angle'] = pitches_out['break_angle'].astype(float)
    pitches_out['break_y'] = pitches_out['break_y'].astype(float)
    pitches_out['break_length'] = pitches_out['break_length'].astype(float)
    
    return pitches_out
    
def load_abs(year, row_limit = 1000000):
    """ loads atbat info from sqlite database stored in same directory """
    
    # open connection to sqlite database
    filename = 'pitchFX_' + str(year) + '.sqlite3'
    db = sqlite3.connect(filename)
    
    # load the pitches in
    abs_out = pd.read_sql('SELECT * FROM atbat LIMIT ' + str(row_limit), db)
    
    return abs_out