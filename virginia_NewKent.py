#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 09:07:51 2022

@author: allison
"""

import pandas as pd



NKparcels = pd.read_excel('assessmentreportNK.xlsx', header=1)

colname = {
    'PID #':'PID', 
    'BAI #':'BAI',
    'GPIN': 'PARCELID',
    'Property Location': 'PROPLOC',
    'Subdivision': 'SUBDIV',
    'Land': 'LAND_ASSESS', 
    'Improvement': 'IMPROV_ASSESS', 
    'Total': 'TOTAL_ASSESS', 
    'City': 'CITY',
    'State': 'STATE',
    'Zip': 'ZIP', 
    'Record Date': 'SALE_DATE',
    'Consideration':'SALE_PRICE',
    'Improved/Vacant': 'IMPROVE_VACANT',
    'Deed Notes': 'DEED', # INCLUDED?
    'Year Built': 'YR_BUILT',
    'Style': 'STYLE',
    'Grade': 'GRADE',
    'Roof Structure': 'ROOF_STRUCT',
    'Roof Cover': 'ROOF_COVER',
    'Ext Wall A': 'EXT_WALLCOV', 
    'Heat Fuel': 'HEAT_FUEL',
    'AC Type': 'AC_TYPE',
    'Int Floor A': 'INT_FLOOR',
    '# of Bedrooms': 'NUM_BED', 
    '# of Baths': 'NUM_BATH',
    'Building Area (Living)': 'LIVING_SQFT', 
    'Land Area (Acres)': 'ACRES', 
    'Zoning': 'ZONING',
    'Utilities': 'UTILITIES',
    'Street/Road': 'STREET_QUALITY'}

NKtrim = NKparcels[colname.keys()]
NKtrim = NKtrim.rename(columns=colname)

NKtrim.to_csv("NKAssessment.csv")
