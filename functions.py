# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 08:32:00 2017

This module stores all the functions required by the filling
missing data tool.

@author: Qingyu.Feng
"""


# Environmental setting
import os
import datetime

# Function 1: Get the list of CSV files in the input folder
def gen_input_csv_list(input_csv_folder):

    input_csv_list = []
    for file in os.listdir(input_csv_folder):
        if file.endswith(".csv"):
            input_csv_list.append(file)

    return input_csv_list
    
# Function 2: Read csv input files
def read_input(input_csv_folder, input_dl_csv):
    fdata = open(input_csv_folder + input_dl_csv, "r")
    dataline = fdata.readlines()
    fdata.close()


    for dlidx in range(len(dataline)):
        dataline[dlidx] = dataline[dlidx].split(",")
        for ddidx in dataline[dlidx]:
            if ddidx == "unknown":
                print(ddidx)
        dataline[dlidx][0] = dataline[dlidx][0][6:]
        dataline[dlidx][-1] = dataline[dlidx][-1][:-1]
        del dataline[dlidx][1]
    del dataline[0]
    
    
    return dataline

# Function : Generating station name list:
def stationlist(dataline):
    stnlstlong = [0]*len(dataline)
    for didx in range(len(dataline)):
        stnlstlong[didx] = str(dataline[didx][0])

    tempset = set(stnlstlong)
    stnlst = list(tempset)

    for sidx in range(len(stnlst)):
        print(stnlst[sidx])

    stn_info_list = 0
    stn_info_list = stnlst*1
    for stnidx in range(len(stn_info_list)):
        for dataidx in dataline:
            if dataidx[0] == stn_info_list[stnidx]:
                stn_info_list[stnidx] = [stn_info_list[stnidx]]\
                                        + dataidx[0:4]
    
    return stnlst, stn_info_list


# Function: Generating station list
def generate_stn_dataline(station, dataline, start_date, 
                          end_date, stn_miss_sum):
    """
    This function generate the data lines for each station
    from the dataline parameter.
    Things that needs to be payed attention to is the 
    missing data.
    Originally, missing data was flagged as -9999 in the downloaded
    files.
    However, the missing days were not marked out.
    For example, in one station, if Jan 26 has no data, the date was 
    directly omited, thus the data was Jan 27 after Jan 25. 
    This needs to be fixed in the time series for model input.
    
    The first step is to get a list of all data for a specific station.
    Then, create a list will full days for each station for the designed 
    period. 
    At last, fill the date of 
    """
    stn_dataline_temp = []
    stn_dataline = []
    stn_missing_temp = {}
    prcp_lst_temp = []
    max_temp_lst_temp = []
    min_temp_lst_temp = []

    prcp_lst = []
    max_temp_lst = []
    min_temp_lst = []


    
    # Generating time series:
    day_start = start_date

    while day_start <= end_date:
        stn_dataline.append([day_start.strftime("%Y%m%d")])
        day_start += datetime.timedelta(days = 1)
        
    for dlidx in dataline:
        if dlidx[0] == station:
            stn_dataline_temp.append(dlidx[4:]) # 4 is the date
            prcp_lst_temp.append(dlidx[5])
            max_temp_lst_temp.append(dlidx[6])
            min_temp_lst_temp.append(dlidx[7])

    print(prcp_lst_temp[0:10])
    print(max_temp_lst_temp[0:10])
    print(min_temp_lst_temp[0:10])

    print("Original stn_dataline_temp length", len(stn_dataline_temp))
    print("Original Prcp length", len(prcp_lst_temp))
    print("Original max temp length", len(max_temp_lst_temp))
    print("Original min temp length", len(min_temp_lst_temp))
    
    # changing missing value from -9999 to -99
    for cidx in range(len(stn_dataline_temp)):
        for scidx in range(len(stn_dataline_temp[cidx])):
            if stn_dataline_temp[cidx][scidx] == "-9999":
                stn_dataline_temp[cidx][scidx] = "-99"

        

    # Matching the date of stn_dataline_temp with dates in stn_dataline.
    # Add the data to the corresponding date, 
    # if there is no data for the date, a -99 was appended.
    for sdidx in range(len(stn_dataline)):
        for sdtidx in range(len(stn_dataline_temp)):
            if (stn_dataline[sdidx][0] == stn_dataline_temp[sdtidx][0]):
                stn_dataline[sdidx] = stn_dataline[sdidx] + stn_dataline_temp[sdtidx]
        if (len(stn_dataline[sdidx]) == 1):
            stn_dataline[sdidx] = stn_dataline[sdidx] + stn_dataline[sdidx] + ["-99", "-99", "-99"]
        
        if stn_dataline[sdidx][2] != "-99":
            stn_dataline[sdidx][2] = (float(stn_dataline[sdidx][2])/10)
        if stn_dataline[sdidx][3] != "-99":
            stn_dataline[sdidx][3] = (float(stn_dataline[sdidx][3])/10)
        if stn_dataline[sdidx][4] != "-99":
            stn_dataline[sdidx][4] = (float(stn_dataline[sdidx][4])/10)
        
        prcp_lst.append(stn_dataline[sdidx][2])
        max_temp_lst.append(stn_dataline[sdidx][3])
        min_temp_lst.append(stn_dataline[sdidx][4])
    
    print("Filled Prcp length", len(prcp_lst))
    print("Filled max temp length", len(max_temp_lst))
    print("Filled min temp length", len(min_temp_lst))
    
    stn_missing_temp = {"stn_name": station,
                        "start_date":stn_dataline_temp[0][0],
                        "end_date":stn_dataline_temp[-1][0],
                        "ori_prcp":prcp_lst_temp.count("-9999"),
                        "ori_maxtemp":max_temp_lst_temp.count("-9999"),
                        "ori_mintemp":min_temp_lst_temp.count("-9999"),

                        "final_prcp":prcp_lst.count("-99"),
                        "final_maxtemp":max_temp_lst.count("-99"),
                        "final_mintemp":min_temp_lst.count("-99")
                        }
    
    stn_miss_sum.append(stn_missing_temp)
    
    return stn_dataline, stn_miss_sum

# Function: Writing output
def write_pt_files(station, stn_dataline, outsubfolder,
                   design_start_date, design_end_date):
    
    
    # write precipitation files
    output_pcp = outsubfolder + "/%sPRCP.txt" %(station)
    fout_pcp = open(output_pcp, "w")
    fout_pcp.writelines(design_start_date + "\n")
    for sdidx in stn_dataline:
        fout_pcp.writelines("%.1f\n" %(float(sdidx[2])))
    fout_pcp.close()
    
    # Write temperature files
    output_tmp = outsubfolder + "/%sTMPC.txt" %(station)
    fout_tmp = open(output_tmp, "w")
    fout_tmp.writelines(design_start_date + "\n")
    for sdidx in stn_dataline:
        if len(sdidx) < 5:
            print(sdidx)
        #print("%.1f,%.1f\n" %(float(sdidx[3]), float(sdidx[4])))
        fout_tmp.writelines("%.1f,%.1f\n" %(float(sdidx[3]), float(sdidx[4])))
    fout_tmp.close()

# Function: writing list
def write_mist_lst(stn_info_list, stn_miss_sum, outsubfolder, input_dl_csv, exp_data_count):
    
    # writing  station missing information 
    stn_miss_sum_wl = [0]*len(stn_miss_sum)
    n_missinginfo = outsubfolder + "/%s_missdatasummary.txt"  %(input_dl_csv[0:6])
    f_missingdatasum = open(n_missinginfo, "w")
    header2 = "StnName,Start,End,OPrcpM,OMaxTM,OMaxTM,FPrcpM,FMaxTM,FMinTM,FPMPent,FMaxTMPent,FMinTMPent\n"
    f_missingdatasum.writelines(header2)
    for midx in range(len(stn_miss_sum)):
        stn_miss_sum_wl[midx] = "%s,%s,%s,%i,%i,%i,%i,%i,%i,%f,%f,%f\n" \
                                %(stn_miss_sum[midx]["stn_name"],
                                  stn_miss_sum[midx]["start_date"],
                                stn_miss_sum[midx]["end_date"],

                                stn_miss_sum[midx]["ori_prcp"],
                                stn_miss_sum[midx]["ori_maxtemp"],
                                stn_miss_sum[midx]["ori_mintemp"],

                                stn_miss_sum[midx]["final_prcp"],
                                stn_miss_sum[midx]["final_maxtemp"],
                                stn_miss_sum[midx]["final_mintemp"],

                                stn_miss_sum[midx]["final_prcp"]/float(exp_data_count)*100,
                                stn_miss_sum[midx]["final_maxtemp"]/float(exp_data_count)*100,
                                stn_miss_sum[midx]["final_mintemp"]/float(exp_data_count)*100
                                    )
        f_missingdatasum.writelines(stn_miss_sum_wl[midx])
        
    f_missingdatasum.writelines("O in front of var name means in original downloaded data\n")
    f_missingdatasum.writelines("F in front of var name means over whole expected period")

    f_missingdatasum.close()

# Function: writing list
def write_stn_lst(stn_info_full, output_folder):
    
    # writing prcp station list 
    prcp_stn_fname = output_folder + "prcpstns.txt"
    fout_prcp_list = open(prcp_stn_fname, "w")
    header = "ID,NAME,LAT,LONG,ELEVATION\n"
    fout_prcp_list.writelines(header)
    for silidx in range(len(stn_info_full)):
        fout_prcp_list.writelines(
                                "%i,%s,%f,%f,%f\n" %(
                                silidx+1, 
                                stn_info_full[silidx][0]+"PRCP",
                                float(stn_info_full[silidx][3]),
                                float(stn_info_full[silidx][4]),
                                float(stn_info_full[silidx][2])))
                                
    fout_prcp_list.close()
    
    # writing temp station list 
    temp_stn_fname = output_folder + "tempstns.txt"
    fout_temp_list = open(temp_stn_fname, "w")
    fout_temp_list.writelines(header)
    for silidx2 in range(len(stn_info_full)):
        fout_temp_list.writelines(
                                "%i,%s,%f,%f,%f\n" %(
                                silidx2+1, 
                                stn_info_full[silidx2][0]+"TMPC",
                                float(stn_info_full[silidx2][3]),
                                float(stn_info_full[silidx2][4]),
                                float(stn_info_full[silidx2][2])))
    fout_temp_list.close()

