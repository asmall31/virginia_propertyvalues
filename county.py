#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 14:31:37 2022

@author: allison
"""

import geopandas as gpd
import matplotlib.pyplot as plt
import os 
# EPSG code for UTM 18N 
utm18n = 26918

out_file = ('NKcounty.gpkg')
# read shape file 
county = gpd.read_file('tl_2021_us_county.zip')
# compare geoid to fips code
on_border = county.query('GEOID == "51127"')
# to_crs goes through and converts to desired projection
on_border = on_border.to_crs(epsg=utm18n)

if os.path.exists(out_file):
    os.remove(out_file)


on_border.to_file(out_file, layer='county', index=False)
