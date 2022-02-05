import matplotlib.pyplot as plt #testing file edit
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
import xlrd2 #the og xlrd doesn't support .xlsx files but this one is more actively maintained
import os #to check directory
import numpy as np
import tkinter as tk
from file2dataset import file2dataset
from dataProcesses import *
import batteryDataSet
global batteryData
global dataSets



#Landt Format
#SHEET_NAMES_LANDT = np.array(['Cycle-Tab','Step-Tab','Record-Tab'])
#COL_NAMES_LANDT = np.array([['Cycle','CapC','CapD','SpeCapC','SpeCapD','Efficiency','EnergyC','EnergyD','MedVoltC','MedVoltD','CC-Cap','CC-Perc',\
	#'PlatCapD','PlatSpeCapD','PlatPercD','PlatTimeD','CaptnC','CaptnD','rd','rd2','SpeEnergyC','SpeEnergyD','EndVoltD','RetentionD','DCIR_C',\
	#'DCIR_D'],\
	#['Step','Mode','Period','Capacity','SpeCap','Power','Capacitance','SpeEnergy','MedVolt','StartVolt','EndVolt','','','','','','','','','',
	#'','','','','',''],\
	#['Record','Test Time',\
	#'Current','Capacity','SpeCap','SOC|DOD','Voltage','Energy','SpeEnergy','AuxTemp','AuxVolt','SysTime','[All Auxiliary-Chl]*','Cycle-Index',\
	#'Step-Index','Step-State','','','','','','','','','']]) #add empty strings for consistent array dimensions

#Arbin Format
#COL_NAMES_ARBIN = np.array(['Data_Point','Test_Time(s)','Date_Time','Step_Time(s)','Step_Index','Cycle_Index','Current(A)','Voltage(V)',\
	#'Charge_Capacity(Ah)','Discharge_Capacity(Ah)','Charge_Energy(Wh)','Discharge_Energy(Wh)','dV/dt(V/s)']) #a few other column names but they aren't typically populated

#import N files with electrochemical datasets
#total_files = 2
#file_names = empty([total_files,2]) #second column to specify number of datasets for each file 

#for fn in range(total_files):
		#find number of datasets in file and construct array
	#	file_names[fn,:] ='ANO Nb doping Data/Half Cell Tests/Temperature Optimization/093_ANO_LNO_700-r2_004_3-1.xlsx'
		
#wb = xlrd2.open_workbook(workbook_location)
#cyclestats=wb.sheet_by_index(0)
#cc = cyclestats.ncols
#dataset=np.array([[float(cyclestats.cell_value(row+1,col)) for col in range(cyclestats.ncols)]for row in range(cyclestats.nrows-2)]) #import data from xlsx spreadsheet to np array format
#cycnum = dataset[1:cyclestats.nrows-1,0] #account for column titles
#spec_caps = dataset[1:cyclestats.nrows-1,2]

def show_plot():
    global dataSets
    plotfig = plt.figure(figsize = (4,4),dpi = 100)
    #ax = plotfig.gca()
    plt.xlabel('Cycle Number')#, fontname='Arial', fontsize=20,labelpad=20)
    #plt.xticks(fontname = 'Arial', fontsize = 12)
    #plt.yticks(fontname = 'Arial', fontsize = 12)
    pane1 = plotfig.add_subplot(111)
    datasetName = selectedData.get()
    print(datasetName)
    pane1.plot(dataSets.get(datasetName)[0],dataSets.get(datasetName)[3],'o',c=[0,0,0]) #this preset should plot specific discharge capacity
    canvas = FigureCanvasTkAgg(plotfig,master = main_window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.RIGHT)
	
def importDataFile():
    global batteryData
    global dataSets
    dataSets = {}
    infile_name = tk.filedialog.askopenfile().name
    batteryData = file2dataset(infile_name)
    dataSets['specific_capacity_data'] = specificCapacity(batteryData.cyclenumbers,batteryData.currentData,batteryData.speCapData)
    dataSets['mean_voltage_data'] = meanVoltage(batteryData.cyclenumbers,batteryData.currentData,batteryData.voltageData)
    print('Ready to plot')

main_window = tk.Tk()
main_window.title('Battery Data Manager')
screen_size = [main_window.winfo_screenwidth(),main_window.winfo_screenheight()]
main_window.geometry("%ix%i" %(screen_size[0]/2,screen_size[1]/2))

plotDataSetButton = tk.Button(main_window,command = show_plot)
plotDataSetButton['text'] = 'Plot Data'
plotDataSetButton.place(relx = 0.1, rely = 0.1, anchor = 'center')

addDataFileButton = tk.Button(main_window,command = importDataFile)
addDataFileButton['text'] = 'Select Data File'
addDataFileButton.place(relx = 0.1, rely = 0.2, anchor = 'center')

selectedData = tk.StringVar(main_window) #the selected string from the dropdown list will be stored in this variable
selectedData.set('Specific Capacity') #this is the default dataset
dataSelect = tk.OptionMenu(main_window, selectedData, 'Specific Capacity', 'Mean Voltage', 'Voltage Curve', 'dQ/dV curve')
dataSelect.place(relx = 0.1, rely = 0.3, anchor = 'center')
dataSelect.config(width = 15)
#show_plot()
main_window.mainloop() #keep window open until closed by used

