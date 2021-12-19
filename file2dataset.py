import xlrd
import numpy as np
from batteryDataSet import BatteryDataSet

def file2dataset(filename):
#this script is dedicated to a function which imports data files
#and outputs a dataset (object of class batteryDataSet) to
#present the data in a consistent way for the rest of the program

#Input: filename(.xlsx)
#Output: batteryDataSet class object
    if filename[-5:] != '.xlsx' and filename[-4:] != '.xls':
        return #add a file type error message in here to be more user friendly
    workbook = xlrd.open_workbook(filename)
    #determine if workbook is Land or Arbin format (could have user indicate this)
    
    

