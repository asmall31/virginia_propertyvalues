#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 17:06:10 2022

@author: allison
"""
import pandas as pd
import geopandas as gpd
NKparcels = gpd.read_file('Virginia_Parcels_(Map_Service).zip')

NKassessment = pd.read_csv('NKAssessment.csv', index_col=False)
# dropping first column where unnamed:0 
NKassessment.drop(list(NKassessment.columns)[0], axis=1, inplace=True)
# merge parcels on assessment on 'PARCELID' in order to combine parcel data on assessment data 
# 'PARCELID' is the same in both csv files 
NKmerge = pd.merge(NKparcels, NKassessment, on='PARCELID')
NKmerge.to_file('NewKentunfiltered.gpkg', layer='merge', index=False)
#%%
# create top 20 land assessment parcel values including non residential
top_nonresparcels = NKmerge.sort_values(by='TOTAL_ASSESS')[-20:]
top_nonresparcels.to_file('TopAssessmentvalues.gpkg', layer='nonresidential', index=False)
# drop values where nan for parcel id 
NKmerge = NKmerge.dropna(subset='PARCELID')

#%%
# drop values where nan for number of beds
# filters down to only residential housing
NKmerge = NKmerge.dropna(subset=['NUM_BED'])
NKmerge.to_file('Residentialproperties.gpkg', layer='residential', index=False)

#%% layer 1
# create new column difference in sale price to assessment which is equal to sale price minus total assessment 
# this will show what value the home was priced at, whether they had a profit on the house or a loss 
NKmerge['DIFF_SP-ASSESS'] = NKmerge['SALE_PRICE']- NKmerge['TOTAL_ASSESS']
# total residential parcels with assessment value 
assessed = NKmerge.dropna(subset=['TOTAL_ASSESS']).copy()


# dropping values where value is nan, ie. there is no value for sale price and or total assessment
total_a_s = NKmerge.dropna(subset=['DIFF_SP-ASSESS']).copy()
# .copy make copy of total_a_s
# write new CSV file where there are values for sales price and total assess
total_a_s.to_csv('Dif_SP-ASSES.CSV')

# write to gqis file make new variable of diff_sp-assess column of total assessment _ sale price


#%% layer 2 top and bottom ten residential parcels

# compute top 10 parcels sorted by highest markup between sale price and assessment
top_city = total_a_s.sort_values(by='DIFF_SP-ASSESS')[-10:]
# compute bottom 10 cities showing 
bottom_city = total_a_s.sort_values(by='DIFF_SP-ASSESS')[:10] 
print(top_city)
print(bottom_city)

top_parcels = top_city['PARCELID']
total_a_s ['topten']= total_a_s['PARCELID'].isin(top_parcels)
# 43 picks out parcel ids of top 10 44 creates new column in data set true if in top 10

bottom_parcels = bottom_city['PARCELID']
total_a_s['bottomten'] = total_a_s['PARCELID'].isin(bottom_parcels)


#%%# layer 3
# drop vacant houses from data set only look at occupied housing 'I' in column IMPROVE/VACANT
occupied = total_a_s.query('IMPROVE_VACANT == "I"')

occupied = occupied['PARCELID']
total_a_s['Occupied'] = total_a_s['PARCELID'].isin(occupied)

# figure this out when repository due 
#percentocc = (occupied/total_a_s)*100

# now total_a_s column Occupied will contain Parcels that people currently live in, can compare to total houses in county


#%% # layer 4 
# look at number of improved houses and the grade of each house
# categories of what houses are what type of grade and total for amount of houses in each grade 
# possibly compare this too total price - assessment see what type of grade was each 

grades = total_a_s[['GRADE']]
grades = grades.sort_values(by='GRADE')
# can you put each grade as a layer on the map


#%% # layer 5
#look at utitlies in houses and get a list of them 
# Filter out nan values 
utilities = total_a_s.dropna(subset=['UTILITIES'])
utilities = utilities['PARCELID']
total_a_s['utilities'] = total_a_s['PARCELID'].isin(occupied)

# add utilites to GQIS map 
# Set index of total_a_s to parcelid
total_a_s = total_a_s.set_index(['PARCELID'])

#%%
layers = total_a_s[['geometry', 'DIFF_SP-ASSESS', 'GRADE', 'YR_BUILT', 'STYLE', 'utilities', 'LIVING_SQFT', 'topten', 'bottomten', 'Occupied']]


# set CRS of layers
#layers = value_layer.set_crs(geometry.crs)
layers.to_file('NewKent.gpkg', layer='values', index=False)




