# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 08:24:31 2017

This code was developed to fill the missing data downloaded from
NCDC webpage
https://gis.ncdc.noaa.gov/map/viewer/#app=cdo&cfg=cdo&theme=daily&layers=111
The data include geographic information, precipitation, max and min temp.
In addition, the downloading included multiple sites. 

The downloaded CSV files contain some errors. Typically two of them
1. the latitude, longitude and elevation might be missing and marked as unknown.
These should be filled manually.
2. The date might be missing and will be filled in the program.


The targeted version of swat model is swat 2012. 
The format of input files include:
1. A list of all input files. The contents in the file looks like:
ID,NAME,LAT,LONG,ELEVATION
1,tmp1,41.56,-93.29,898

2. One file for each station. The contents in the file looks like:
20050101 (Startind date of the station)
1.9,-5.3 (max, min temperature, or precipitation as one value)
1.2,-3.1
-3.2,-5.4
The name of files for each station will be listed in the list file.



Steps of finishing these operations include:
    1. Readin the inputs from a single CVS file (stored in a folder)
    2. Get a list of stations containing in the CVS file.
    3. Read each csv files, comparing to a complete
    date list, and count the number and percentage of missing data.
    4. also, generate one file for each station in the format of 
    SWAT input for filling purpose.
    
    This is the second stage
    5. Filling the missing data stations using IDW. This depends on
    the distance matrix (Tutorial below).
    The missing stations are kept for now because they can be used to
    data for remaining statins that has less than 25% missing data.
    
    
Generating distance matrix
    1. Add layer to QGIS using add delimited text layer as instructed in
    http://www.qgistutorials.com/en/docs/importing_spreadsheets_csv.html
    2. Export the stations to shapefile for future reference
    3. Calculate the distance matrix using Vector -> Analysis tool ->
    Distance Matrix. 
    Chose the input point layer and target point layer both as the station
    shapefile. Chose ID as name of the stations.
    Output matrix type: check Standard (N x T) distance matrix.
    4. Run another script (01_main_idw.py) to fill the data.

@author: Qingyu.Feng
"""

# Enviornment settings
from __future__ import print_function
import datetime
import os
from functions import *
import shutil


########################################################################
# Inputs and output names:
infdn_ncdccvs = "00_downloadedcvs" + "/"
outfdn1_unfilled = "temp_run1_unfilled" + "/"


# Check whether output folder exists
if not os.path.isdir(infdn_ncdccvs):
    print("warning: please check input folder or the folder name!!" )
    
if not os.path.isdir(outfdn1_unfilled):
    os.mkdir(outfdn1_unfilled)
########################################################################


########################################################################
# Input variables:
design_start_date = "19910101"
design_end_date = "20101231"

# Convert start and end date for comparison
start_date = datetime.date(int(design_start_date[0:4]),
                            int(design_start_date[4:6]),
                            int(design_start_date[6:8]))

end_date = datetime.date(int(design_end_date[0:4]),
                            int(design_end_date[4:6]),
                            int(design_end_date[6:8]))

exp_data_count = (end_date - start_date).days

########################################################################

########################################################################
# Calling functions

# Variable define 
stn_info_full = []


# Get CSV file name list
input_csv_list = gen_input_csv_list(infdn_ncdccvs)

# read dataline in each csv files
for input_dl_csv in input_csv_list:
    
    print("Data is being extracted from file: ", input_dl_csv)
    
    # Generate folder for each csv file.
    outsubfolder = outfdn1_unfilled + "csv_%s" % (input_dl_csv[0:-4])
    if not os.path.isdir(outsubfolder):
        os.mkdir(outsubfolder)
    else:
        shutil.rmtree(outsubfolder)
        os.mkdir(outsubfolder)
        
    # reset dataline to empty
    dataline = []
    # Reading the whole dataline
    dataline = read_input(infdn_ncdccvs, input_dl_csv)
   
    print("Generating station list")
    stnlst, stn_info_list = stationlist(dataline)

    print(stnlst)

    stn_info_full = stn_info_full + stn_info_list


    # A new list was generated to record the information of each station
    stn_miss_sum = []

    for station in stnlst:
        print("processing station: ", station)

        print ("gererating station data lines")

        stn_dataline, stn_miss_sum = generate_stn_dataline(station, 
                                                           dataline,
                                                           start_date,
                                                           end_date, 
                                                           stn_miss_sum)

        print("Writing station files")
        write_pt_files(station, stn_dataline, outsubfolder,
                       design_start_date, design_end_date)

    #Writing station list files
    write_mist_lst(stn_info_list, 
                   stn_miss_sum, 
                   outsubfolder, 
                   input_dl_csv,
                   exp_data_count)

write_stn_lst(stn_info_full, outfdn1_unfilled)

