import xlrd2
import numpy as np
from batteryDataSet import batteryDataSet

def file2dataset(filename):
#this script is dedicated to a function which imports data files
#and outputs a dataset (object of class batteryDataSet) to
#present the data in a consistent way for the rest of the program

#Input: filename(.xlsx)
#Output: batteryDataSet class object
    COL_NAMES_LAND = [['Cycle','SpeCapC/mAh/g','SpeCapD/mAh/g','Efficiency/%','MedVoltC/V','MedVoltD/V'],['','','','','',''],
        ['SpeCap/mAh/g','Voltage/V','Cycle-Index','Step-Index','TestTime','Current/mA']] #add empty strings for consistent array dimensions

    COL_NAMES_ARBIN = np.array(['Step_Index','Cycle_Index','Current(A)','Voltage(V)','Charge_Capacity(Ah)','Discharge_Capacity(Ah)', 'Test_Time(s)'])

    if filename[-5:] != '.xlsx' and filename[-4:] != '.xls':
        return #add a file type error message in here to be more user friendly
    workbook = xlrd2.open_workbook(filename)
    #determine if workbook is Land or Arbin format (could have user indicate this)
    #Land format if Tab names contain 'Tab'; assume Arbin otherwise
    sysFormat = "Arbin"
    if 'Tab' in workbook.sheet_names()[0]:
        sysFormat = "Land"
    if sysFormat == "Land":
        sheets = workbook.sheet_names()
        tabColNames = [None for y in range(len(sheets))]
        header_dict={} #for Land system, expect 1 dataset per file so this can be initialized outside the loop
        for i in range(len(sheets)):
            tabColNames[i] = workbook.sheet_by_index(i).row_values(0) #list of all data column titles in input file
            for dataColName in COL_NAMES_LAND[i]: 
                if dataColName in tabColNames[i] and dataColName != '': #iterate over all data columns in input file which are recognized by batteryDataSet class
                    header_dict[dataColName+str(i)] = workbook.sheet_by_index(i).col_values(tabColNames[i].index(dataColName),1) #construct dictionary associating column titles with datasets
        dataset_obj = batteryDataSet(sysFormat='Land',data_header_dictionary=header_dict) #get batteryDataSet object
    elif sysFormat == "Arbin":
        sheets=workbook.sheet_names()
        #for sheet in sheets:
            #if '-' not in sheet.split('_')[-1]:
                #dataset_sheet_num = int(sheet.split('_')[-1])
                 
        datasets = [sheet for sheet in sheets if 'Channel' in sheet] #how to handle large datasets occupying multiple sheets?
        dataset_obj = [None for dataset in range(len(datasets))]
        tabColNames = [None for sheet in range(len(datasets))]
        for i in range(len(datasets)):
            tabColNames[i] = workbook.sheet_by_name(datasets[i]).row_values(0)
            header_dict={} #for Arbin multiple datasets per file may be expected so this is re-initialized on each loop iteration to create a batteryDataSet object for each sheet
            for dataColName in COL_NAMES_ARBIN:
                header_dict[dataColName] = workbook.sheet_by_name(datasets[i]).col_values(tabColNames[i].index(dataColName),1) 
            dataset_obj[i] = batteryDataSet(sysFormat='Arbin',data_header_dictionary=header_dict) #construct array of batteryDataSet object with 1 entry per cell

    return dataset_obj

