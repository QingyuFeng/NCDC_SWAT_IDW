# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 13:42:40 2017

Goal:
    1. To fill missing data based on the nearest 5 stations using the
    inverse distance weighting method.



@author: Qingyu.Feng
"""
########################################################################
# Enviornment settings
from __future__ import print_function
import datetime
import os
from collections import OrderedDict
from operator import itemgetter
from functions_idw import *
########################################################################

########################################################################
# Inputs and output names:

# Distance file folders:
distancefolder = "01_distancematrix/"

# Distance related files
distancematrix = "distancematrix_allstns_05_16.csv"

# Input SWAT Input folder
input_unfilled_folder = "temp_run1_unfilled/csv_1038309_1991_2010/"
output_filled_folder = "temp_run2_filled_05_16/"

# Check whether output folder exists
if not os.path.isdir(input_unfilled_folder):
    print("warning: please check input folder or the folder name!!" )
    
if not os.path.isdir(output_filled_folder):
    os.mkdir(output_filled_folder)

########################################################################

########################################################################
# Calling functions:
dist_id, dist_lines = get_distance(distancefolder, distancematrix)

get_near_stns(dist_id, dist_lines)

open_stn_files(dist_id, 
               dist_lines, 
               input_unfilled_folder,
               output_filled_folder)

