# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 13:45:18 2017

Containing functions for doing IDW filling


@author: Qingyu.Feng
"""
from __future__ import print_function
import datetime
import os
from collections import OrderedDict
from operator import itemgetter



# Functions
def get_distance(distancefolder, distancematrix):
       
    # read in distance list
    dist_data = open(distancefolder + distancematrix, "r")
    dist_lines = dist_data.readlines()
    dist_data.close()
    
    dist_id = dist_lines[0].split(",")
    dist_id[-1] = dist_id[-1][0:-1]

    del dist_lines[0]

    for dlidx in range(len(dist_lines)):
        dist_lines[dlidx] = dist_lines[dlidx].split(",")
        
        for dlsidx in range(1, len(dist_lines[dlidx])):
            dist_lines[dlidx][dlsidx] = float(dist_lines[dlidx][dlsidx])

    return dist_id, dist_lines


def get_near_stns(dist_id, dist_lines):

    for dlidx in range(len(dist_lines)):        

        dist_lines[dlidx] = dict(zip(dist_id ,dist_lines[dlidx]))
        dist_lines[dlidx] = [(k,v) for v, k in sorted([(v, k) for k, v in dist_lines[dlidx].items()])][0:6]
   
    

def open_stn_files(dist_id, 
                   dist_lines, 
                   input_unfilled_folder,
                   output_filled_folder):

    # Open unfilled files and read in data for targeted station and reference station.
    for dlidx in range(len(dist_lines)):
        print("Processing No.", dlidx, " stations")
        print(dist_lines[dlidx])
        
        target_stn_prcp = [0]
        ref_stn_1 = [0]
        ref_stn_2 = [0]
        ref_stn_3 = [0]
        ref_stn_4 = [0]
        ref_stn_5 = [0]

        for distidx in dist_id:
            if dist_lines[dlidx][0][0] == distidx:
                
                ftarget = open(input_unfilled_folder + distidx + ".txt", "r")
                target_stn_prcp = ftarget.readlines()
                ftarget.close()
               
                for tidx in range(1, len(target_stn_prcp)):
                    target_stn_prcp[tidx] = float(target_stn_prcp[tidx][:-1])

            if dist_lines[dlidx][1][0] == distidx:
                
                fref1 = open(input_unfilled_folder + distidx + ".txt", "r")
                ref_stn_1 = fref1.readlines()
                fref1.close()

                for r1idx in range(1, len(ref_stn_1)):
                    ref_stn_1[r1idx] = float(ref_stn_1[r1idx][:-1])

            if dist_lines[dlidx][2][0] == distidx:
                
                fref2 = open(input_unfilled_folder + distidx + ".txt", "r")
                ref_stn_2 = fref2.readlines()
                fref2.close()

                for r2idx in range(1, len(ref_stn_2)):
                    ref_stn_2[r2idx] = float(ref_stn_2[r2idx][:-1])

            if dist_lines[dlidx][3][0] == distidx:
                
                fref3 = open(input_unfilled_folder + distidx + ".txt", "r")
                ref_stn_3 = fref3.readlines()
                fref3.close()

                for r3idx in range(1, len(ref_stn_3)):
                    ref_stn_3[r3idx] = float(ref_stn_3[r3idx][:-1])

            if dist_lines[dlidx][4][0] == distidx:
                
                fref4 = open(input_unfilled_folder + distidx + ".txt", "r")
                ref_stn_4 = fref4.readlines()
                fref4.close()

                for r4idx in range(1, len(ref_stn_4)):
                    ref_stn_4[r4idx] = float(ref_stn_4[r4idx][:-1])

            if dist_lines[dlidx][5][0] == distidx:
                
                fref5 = open(input_unfilled_folder + distidx + ".txt", "r")
                ref_stn_5 = fref5.readlines()
                fref5.close()

                for r5idx in range(1, len(ref_stn_5)):
                    ref_stn_5[r5idx] = float(ref_stn_5[r5idx][:-1])

            # Calculating the IDW value for this target stn series
            # Then, determine whether the ref has missing values.
            # If there are, the station will be dropped.
            # This tuple need to be cleared for each day.
        
        for caltidx in range(1, len(target_stn_prcp)):
            if target_stn_prcp[caltidx] == -99:
                
                daily_dist_value = []
                ref_nomiss = []
            
                daily_dist_value = dist_lines[dlidx]*1
                
                daily_dist_value[0] = daily_dist_value[0] + (target_stn_prcp[caltidx],)
                daily_dist_value[1] = daily_dist_value[1] + (ref_stn_1[caltidx],)
                daily_dist_value[2] = daily_dist_value[2] + (ref_stn_2[caltidx],)
                daily_dist_value[3] = daily_dist_value[3] + (ref_stn_3[caltidx],)
                daily_dist_value[4] = daily_dist_value[4] + (ref_stn_4[caltidx],)
                daily_dist_value[5] = daily_dist_value[5] + (ref_stn_5[caltidx],)
                
                ref_nomiss = [s for s in daily_dist_value[1:] if s[2] != -99]
                daily_dist_value = [daily_dist_value[0]] + ref_nomiss
            
                
                # Calculate the idw for days with -99 values

                dist_fraction = [0]*(len(daily_dist_value))
                dist_fraction_times_prcp = [0]*(len(daily_dist_value))

                sum_frac = 0
                sum_frac_prcp = 0
                for ddvidx in range(1, len(daily_dist_value)):
                    # first calculate the fraction of distance
                    dist_fraction[ddvidx] = 1/daily_dist_value[ddvidx][1]
                    # Then calculate the product of distance fraction and precipitation values
                    dist_fraction_times_prcp[ddvidx] = dist_fraction[ddvidx] * daily_dist_value[ddvidx][2]

                
                sum_frac = sum(dist_fraction)
                sum_frac_prcp = sum(dist_fraction_times_prcp)

                if (sum_frac == 0):
                    sum_frac = 1
                    sum_frac_prcp = -99
                    

    
                target_stn_prcp[caltidx] = sum_frac_prcp/sum_frac
            else:
                target_stn_prcp[caltidx] = target_stn_prcp[caltidx]

        # Write output files with filled target stn precipitation values:
        fout = open(output_filled_folder + dist_lines[dlidx][0][0] +".txt", "w")
        fout.writelines(target_stn_prcp[0])
        for tspwidx in range(1, len(target_stn_prcp)):
            fout.writelines("%.1f\n"  %(target_stn_prcp[tspwidx]))
        fout.close()