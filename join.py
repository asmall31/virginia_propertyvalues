#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 10 22:46:38 2022

@author: allison
"""

import geopandas as gpd

parcels = gpd.read_file('NewKentunfiltered.gpkg')
bgs = gpd.read_file('NKdemographics.gpkg')

centroids = parcels.copy()
centroids['geometry'] = parcels.centroid

merged = centroids.sjoin(bgs,how='left',predicate='within')

print('ideally, these are equal:', len(centroids), len(merged) )

cols = list(bgs.columns)


merged = merged[cols]

parcels_plus = parcels.sjoin(merged,how='left',predicate='contains')

print('ideally, these are equal:', len(parcels), len(parcels_plus) )

parcels_plus.to_file('parcels_plus.gpkg',layer='parcels',index=False)