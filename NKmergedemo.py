#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  6 14:44:51 2022

@author: allison
"""

import pandas as pd
import geopandas as gpd


# read in the demographic data
demographics = pd.read_csv("NKdemo.csv", dtype={'GEOID':str})

demographics = demographics.set_index(['GEOID'])
# percentage of total population that is white
demographics['percwhite'] = (demographics['total_pop_white']/demographics['total_pop'])*100
# percent of the total population that is black 
demographics['percblack'] = (demographics['total_pop_black']/demographics['total_pop'])*100
# percent of the total population that is american indian
demographics['percamericanindian'] = (demographics['total_pop_americanindian']/demographics['total_pop'])*100
# percent of the total population that is asian 
demographics['percblack'] = (demographics['total_pop_asian']/demographics['total_pop'])*100

# percentage of total homes that are owned
demographics['percowned'] = (demographics['housing_owned']/demographics['housing_total'])*100
# percentage of total homes that are rented
demographics['percrented'] = (demographics['housing_rental']/demographics['housing_total'])*100




#%%
# read in block group shapefile and merge to demographic data
# bgs is block group shapefile
bgs = gpd.read_file('tl_2021_51_bg (2).zip')
# filter bgs to New Kent county by using query method where record equal to county code
bgs = bgs.query('COUNTYFP== "127"')

keep_cols = ['GEOID', 'COUNTYFP', 'geometry']
# set bgs to keeping columns 
bgs = bgs[keep_cols]

# calculate area of each block group, .area is not a function, no ()
bgs['bg_area'] = bgs.area
# merge bgs to pop data
bgs = bgs.merge(demographics, on='GEOID', validate='1:1', indicator=True)

print(bgs['_merge'].value_counts())
bgs.drop(columns=['_merge'],inplace=True)

bgs.to_file('NKdemographics.gpkg', layer='demographics', index=False)
