import matplotlib.pyplot as plt  # testing file edit
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import xlrd2  # the og xlrd doesn't support .xlsx files but this one is more actively maintained
import os  # to check directory
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
    global dataSets, batteryData
    if batteryData[0].sysFormat == 'Arbin':
        if selectedEntryMode.get() == 'Calculate:':
            # print(np.nonzero(batteryData[0].currentData))
            print(mass_entry.get())
            active_mass = batteryData[0].currentData[np.nonzero(batteryData[0].currentData)[0][2]] / (float(
                mass_entry.get()) * 0.180)  # 180 mAh/g assumed initially, add input options for this later
        elif selectedEntryMode.get() == 'Enter Mass Manually:':
            active_mass = float(mass_entry.get()) / 1000  # assume entry in mg
        batteryData[0].recalculate(active_mass)
        for dataset in range(num_datasets):
            dataSets[dataset]['Specific Capacity'] = specificCapacity(batteryData[dataset].cyclenumbers,
                                                                      batteryData[dataset].currentData,
                                                                      batteryData[dataset].speCapData)
            dataSets[dataset]['Mean Voltage'] = meanVoltage(batteryData[dataset].cyclenumbers,
                                                            batteryData[dataset].currentData,
                                                            batteryData[dataset].voltageData)
            dataSets[dataset]['Voltage Curve'] = voltageCurve(3, batteryData[dataset].cyclenumbers,
                                                              batteryData[dataset].speCapData,
                                                              batteryData[dataset].voltageData)
            dataSets[dataset]['dQ/dV curve'] = dQdVcurve(3, batteryData[dataset].cyclenumbers,
                                                         batteryData[dataset].speCapData,
                                                         batteryData[dataset].voltageData)
    plotfig = plt.figure(figsize=(6, 4), dpi=100)
    # ax = plotfig.gca()
    # plt.xticks(fontname = 'Arial', fontsize = 12)
    # plt.yticks(fontname = 'Arial', fontsize = 12)
    pane1 = plotfig.add_subplot(1, 1, 1)
    datasetName = selectedData.get()
    if datasetName == "Specific Capacity":
        # apply default format settings for specific capacity plot
        pane1.plot(dataSets[0].get(datasetName)[0], dataSets[0].get(datasetName)[1], '.', c=[0, 0, 0])
        pane1.set_xlabel('Cycle Number', fontname = 'Arial', fontsize=10)
        pane1.set_ylabel('Specific Discharge Capacity (mAh / g)', fontname='Arial', fontsize=10)
        pane1.set_title('Specific Capacity',fontname = 'Arial', fontsize = 12)

    elif datasetName == "Mean Voltage":
        pane1.plot(dataSets.get(datasetName)[0],dataSets.get(datasetName)[1],'o',c=[0,0,0])
        pane1.plot(dataSets.get(datasetName)[0],dataSets.get(datasetName)[2],'*',c=[0,0,0])
        pane1.set_xlabel('Cycle Number',fontname='Arial',fontsize=10)
        pane1.set_ylabel('Mean Voltage (V)',fontname='Arial',fontsize=10)

    elif datasetName == "Voltage Curve": 
        cycle_numbers_string = set_cycle_numbers.get() #retrieve user input providing cycle numbers
        #convert string input to list of integers
        cycle_numbers_strings = cycle_numbers_string.split(",") #splits input into cycle numbers
        cycle_numbers = []
        for cycle in cycle_numbers_strings:
            try:
                cycle_numbers.append(int(cycle)) #checks if cycle numbers are valid integers
            except:
                print("Please enter valid input. This is a list of comma separated integers.")

		#Step 1: validate input (a comma-separated list of integers is an acceptable input)
		#Step 2: convert string input to a list (e.g. numpy array) of cycle numbers to be plotted
		#Step 3: obtain dataset for each cycle specified and add to plot
        #symbols = ['o', '*', '.']
        colors = [(0,0,0),(0.5,0,0), (0,0.5,0), (0,0,0.5), (0.5,0.5,0), (0,0.5,0.5), (0.5,0,0.5)] #normalize color code values to 255
        counter = 7
        for i in range(len(cycle_numbers)):
            #s = counter % 3
            c = counter % 7 #allows for changing colors between graphs
            cycle_label = 'Cycle ' + str(cycle_numbers[i]) #generates cycle label as neccessary
            dataSets[0]['Voltage Curve'] = voltageCurve(cycle_numbers[i],batteryData[0].cyclenumbers,batteryData[0].speCapData,batteryData[0].voltageData)
            pane1.plot(dataSets[0].get(datasetName)[0].squeeze(),dataSets[0].get(datasetName)[1].squeeze(),'.',c=colors[c], label=cycle_label) #check if adding to data on plot or overwriting previous
            counter += 1
        pane1.set_xlabel('Specific Capacity (mAh / g)',fontname='Arial',fontsize=12)
        pane1.set_ylabel('Voltage (V)',fontname='Arial',fontsize=12)
        pane1.legend()

    elif datasetName == "dQ/dV curve":
        cycle_numbers_string = set_cycle_numbers.get()  # retrieve user input providing cycle numbers
        # convert string input to list of integers
        cycle_numbers_strings = cycle_numbers_string.split(",")
        cycle_numbers = []
        for cycle in cycle_numbers_strings:
            try:
                cycle_numbers.append(int(cycle))
            except:
                print("Please enter valid input. This is a list of comma separated integers.")
            # Step 1: validate input (a comma-separated list of integers is an acceptable input)
            # Step 2: convert string input to a list (e.g. numpy array) of cycle numbers to be plotted
            # Step 3: obtain dataset for each cycle specified and add to plot
        # symbols = ['o', '*', '.']
        colors = [(0, 0, 0), (0.5, 0, 0), (0, 0.5, 0), (0, 0, 0.5), (0.5, 0.5, 0), (0, 0.5, 0.5),
                  (0.5, 0, 0.5)]  # normalize color code values to 255
        counter = 8
        for i in range(len(cycle_numbers)):
            # s = counter % 3
            c = counter % 7
            cycle_label = 'Cycle ' + str(cycle_numbers[i])
            dataSets[0]['dQ/dV curve'] = dQdVcurve(cycle_numbers[i], batteryData[0].cyclenumbers, batteryData[0].speCapData,
                                               batteryData[0].voltageData)
            pane1.plot(dataSets[0].get(datasetName)[0], dataSets[0].get(datasetName)[1], '.', c=colors[c], label=cycle_label)
            counter += 1
        pane1.set_xlabel('Voltage (V)', fontname='Arial', fontsize=12)
        pane1.set_ylabel('dQ/dV (mAh / g / V)', fontname='Arial', fontsize=10)
        pane1.legend()
    else:
       pass
    canvas = FigureCanvasTkAgg(plotfig,master = main_window)
    canvas.draw()
    canvas.get_tk_widget().grid(column = 1, row = 1, columnspan = 2, rowspan = 2)
	
def importDataFile():
    global batteryData
    global dataSets
    global num_datasets
    global max_cycle
    global data_selected
    infile_name = tk.filedialog.askopenfile().name
    import_control = tk.Label(controlframe, text=infile_name[-20:], bg="#cfe2f3")
    import_control.grid(column=1, row=2, columnspan=2, padx=5, pady=5)
    batteryData = file2dataset(infile_name)
    # num_datasets = 1
    if not isinstance(batteryData, list):
        Format = batteryData.sysFormat
        dataSets = {}
        dataSets['Specific Capacity'] = specificCapacity(batteryData.cyclenumbers, batteryData.currentData,
                                                         batteryData.speCapData)
        dataSets['Mean Voltage'] = meanVoltage(batteryData.cyclenumbers, batteryData.currentData,
                                               batteryData.voltageData)
        dataSets['Voltage Curve'] = voltageCurve(3, batteryData.cyclenumbers, batteryData.speCapData,
                                                 batteryData.voltageData)
        dataSets['dQ/dV curve'] = dQdVcurve(3, batteryData.cyclenumbers, batteryData.speCapData,
                                            batteryData.voltageData)
        max_cycle = max(BatteryData.cyclenumbers)
    else:  # list type dataset from arbin
        Format = batteryData[0].sysFormat
        num_datasets = len(batteryData)
        dataSets = [{} for x in range(num_datasets)]
        for dataset in range(num_datasets):
            dataSets[dataset]['Specific Capacity'] = specificCapacity(batteryData[dataset].cyclenumbers,
                                                                      batteryData[dataset].currentData,
                                                                      batteryData[dataset].speCapData)
            dataSets[dataset]['Mean Voltage'] = meanVoltage(batteryData[dataset].cyclenumbers,
                                                            batteryData[dataset].currentData,
                                                            batteryData[dataset].voltageData)
            # dataSets[dataset]['Voltage Curve'] = voltageCurve(3,batteryData[dataset].cyclenumbers,batteryData[
            # dataset].speCapData,batteryData[dataset].voltageData) dataSets[dataset]['dQ/dV curve'] = dQdVcurve(3,
            # batteryData[dataset].cyclenumbers,batteryData[dataset].speCapData,batteryData[dataset].voltageData)
        mass_entry['state'] = tk.NORMAL
        max_cycle = max(batteryData[dataset].cyclenumbers)

    print('Detected %s file format' % Format)
    print('%d dataset(s) imported' % num_datasets)
    print('Ready to Plot')
    plotDataSetButton['state'] = tk.NORMAL
    data_selected = True



def onSelectData(self):
    if (selectedData.get() == 'Voltage Curve' or selectedData.get() == 'dQ/dV curve') and data_selected == True:
        set_cycle_numbers['state'] = tk.NORMAL
        message = "(Max Cycle: " + str(int(max_cycle)) + ")"
        set_cycle_numbers.delete(0, tk.END)
        set_cycle_numbers.insert(0, message)
        #set_cycle_numbers_prompt['state'] = tk.NORMAL
    else:
        set_cycle_numbers['state'] = tk.DISABLED
        #set_cycle_numbers_prompt['state'] = tk.DISABLED

def onSelectEntryMode(self):
    if selectedEntryMode.get() == 'Enter Mass Manually:':
        mass_entry.delete(0, tk.END)
        mass_entry.insert(0, 'Enter mass (mg)')
    elif selectedEntryMode.get() == 'Calculate:':
        # theor_capac_entry['state'] = tk.NORMAL
        mass_entry.delete(0, tk.END)
        mass_entry.insert(0, '0.1')
        # make prompts & extra textbox active

def multiCurve(x_datasets,y_datasets,cycle_numbers = [1]):
    # returns datasets corresponding to specified cycle numbers
    # mainly for voltage and dqdv curve plotting
    cycle_dataSets = np.empty([len(cycle_numbers),2]).squeeze()
    for index in range(len(cycle_numbers)):
        cycle_dataSets[index] = (np.array([x_datasets[cycle_numbers[index]],y_datasets[cycle_numbers[index]]]))
    return cycle_dataSets
main_window = tk.Tk()
main_window.title('Battery Data Manager')
screen_size = [main_window.winfo_screenwidth(),main_window.winfo_screenheight()]
main_window.geometry("%ix%i" %(screen_size[0]*3/4,screen_size[1]*3/4))

#control frame
controlframe = tk.Frame(main_window,bg="#0b60ad")
controlframe.grid(column = 0, row = 0, padx = 10, pady = 10, ipadx = 10, ipady = 10)

import_control = tk.Label(controlframe,text = "File and Dataset Control", bg = "#9fc5e8")
import_control.grid(column = 0, row = 0, columnspan = 2, padx = 5, pady = 5)

plotDataSetButton = tk.Button(controlframe,command = show_plot,state=tk.DISABLED)
plotDataSetButton['text'] = 'Plot Data'
plotDataSetButton.grid(column = 0,row = 1,padx = 5, pady = 5)
#plotDataSetButton.place(relx = 0.1, rely = 0.1, anchor = 'center')

addDataFileButton = tk.Button(controlframe,command = importDataFile)
addDataFileButton['text'] = 'Select Data File'
addDataFileButton.grid(column = 0,row = 2,padx = 5,pady = 5)
#addDataFileButton.place(relx = 0.1, rely = 0.2, anchor = 'center')

selectedEntryMode = tk.StringVar(main_window)
selectedEntryMode.set('Calculate (enter initial C-rate):')
mass_entry_mode = tk.OptionMenu(controlframe, selectedEntryMode, 'Enter Mass Manually:', 'Calculate:',
                                command=onSelectEntryMode)
mass_entry_mode.grid(column = 0,row = 4, padx = 5, pady = 5)
#mass_entry_mode.place(relx=0.15, rely=0.4, anchor='center')
mass_entry_mode.config(width=25)
mass_entry = tk.Entry(controlframe)
mass_entry.insert(0,"Active Mass (mg):")
mass_entry.grid(column = 1, row = 4, padx = 5, pady = 5)
#theor_capac_entry = tk.Entry(controlframe)
#theor_capac_entry.insert(0,"Capacity (mAh/g):")
#theor_capac_entry.grid(column = 1, row = 4, padx = 5, pady = 5)

selectedData = tk.StringVar(main_window) #the selected string from the dropdown list will be stored in this variable
selectedData.set('Specific Capacity') #this is the default dataset
dataSelect = tk.OptionMenu(controlframe, selectedData, 'Specific Capacity', 'Mean Voltage', 'Voltage Curve', 'dQ/dV curve',command = onSelectData)
dataSelect.grid(column = 0, row = 3, padx = 5, pady = 5)
#dataSelect.place(relx = 0.1, rely = 0.3, anchor = 'center')
dataSelect.config(width = 15)

set_cycle_numbers = tk.Entry(controlframe)
set_cycle_numbers.insert(0,"Cycle number(s):")
set_cycle_numbers.grid(column = 1,row = 3)

#formatframe
formatFrame = tk.Frame(main_window, bg = "#674ea7")
formatFrame.grid(column = 0, row = 1, padx = 10, pady = 10, ipadx = 10, ipady = 10)

graph_control = tk.Label(formatFrame,text = "Graph Control", bg = "#b4a7d6")
graph_control.grid(column = 0, row = 0, columnspan = 2, padx = 5, pady = 5)


#show_plot()
main_window.mainloop() #keep window open until closed by user

