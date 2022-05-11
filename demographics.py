#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  2 18:40:10 2022

@author: allison
"""


import pandas as pd
import geopandas as gpd
import requests 
import numpy as np
# import census data for American Communial Survey
#api = 'https:api.census.gov/data/2019/acs/acsse?'

demographics = {
    # race
    'B02001_001E': 'total_pop',
    'B02001_002E': 'total_pop_white',
    'B02001_003E': 'total_pop_black',
    'B02001_004E': 'total_pop_americanindian',
    'B02001_005E': 'total_pop_asian',
    # 
    'B01001_001E' : 'sex_by_age',
    # median age by sex
    'B01002_001E': 'median_age',
    # housing
 'B25003_001E': 'housing_total',
 'B25003_002E': 'housing_owned',
 'B25003_003E': 'housing_rental',
 # median earnings in the past 12 months
 'B20002_001E': 'earnings',
    # presence of own children
    'B23003_001E' : 'presence_children',
    }
#%%

variables  = demographics.keys()
get_clause = ','.join(variables)

api = "https://api.census.gov/data/2020/acs/acs5" 

for_clause = 'block group:*'
# 'in' clause used to limit select geographic data
# Virginia state #51 New Kent fips #51127
in_clause = 'state:51 county:127' 

key_value = 'd008e01ad45b4ef1f4c72ce47bf0a04fd3d72a96'
payload = {'get':get_clause,'for':for_clause, 'in':in_clause, 'key':key_value}

response = requests.get(api, payload) 

if response.status_code == 200:
    print(f'If the request was successful')
else:
    print(response.status_code)
    print(response.text)
    assert False 
  
        # cause script to stop if statement reached
    #%%            
row_list = response.json()  
# parse JSON returned by census server return list of rows
# first row of row_list
colnames = row_list[0]

datarows = row_list[1:] #remianing rows

NKdemo = pd.DataFrame(columns=colnames, data=datarows)

# deal with missing data in pop
NKdemo = NKdemo.replace("-666666666", np.nan)
# rename dictionary from line 14
NKdemo.columns = list(demographics.values())+['state','county','tract','block group']
#NKdemo = NKdemo.rename(columns=list(demographics.values()))
# new column of pop GEOID which brings together state, county, tract and block group
NKdemo["GEOID"] = NKdemo['state']+''+NKdemo["county"]+''+NKdemo['tract']+''+NKdemo['block group']

NKdemo = NKdemo.set_index(['GEOID'])

keep_cols = list(demographics.values())

NKdemo = NKdemo[keep_cols]

NKdemo.to_csv('NKdemo.csv')


