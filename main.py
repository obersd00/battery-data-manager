import matplotlib.pyplot as plt  # testing file edit
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import xlrd2  # the og xlrd doesn't support .xlsx files but this one is more actively maintained
import os  # to check directory
import numpy as np
import tkinter as tk
from tkinter import ttk
from file2dataset import file2dataset
from dataProcesses import *
import matplotlib as mpl
import logging
logging.getLogger('matplotlib.font_manager').disabled = True #because it prints out a tone of warnings if the selected font is not found
from Graphing import plotSpecCapCurves, plotMeanVoltageCurves, plotVoltCurves, plotdQdVCurves, plotCoulombicEfficiencyCurves
from Export2Excel import createSheet
import batteryDataSet
from pickle import dump,load
global batteryData
global dataSets
global max_cycle
global max_cycle_list
global plotfig
global fontEntryMode
global is_bdms
global combined_bdms_files
global dataset_selection
global data_selection_tabs
global dataset_checkboxes

is_bdms = False
combined_bdms_files = []
data_selection_tabs = []
dataset_selection = []
dataset_checkboxes = []

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
    global dataSets, batteryData, active_mass, nominal_capacity, combined_bdms_files, is_bdms, dataset_selection
    try:
        nominal_capacity = int(set_nominal_capacity.get())
    except:
        nominal_capacity = 180
        set_nominal_capacity.delete(0, tk.END)
        set_nominal_capacity.insert(0, "180")
    font = chooseFont()
    titleSize, axesSize, legendSize, tickSize = fontScale(title_font_size_scale, axes_font_size_scale, legend_font_size_scale, ticks_font_size_scale)

    if batteryData[0].sysFormat == 'Arbin' or batteryData[0].sysFormat == 'Land':
        if selectedEntryMode.get() == 'Calculate (enter initial C-rate):':
            # print(np.nonzero(batteryData[0].currentData))
            acive_masses = []
            if batteryData[0].sysFormat == 'Arbin':
                for file in combined_bdms_files:
                    for dataset in range(len(file)):
                        active_mass = abs(file[dataset].currentData[np.nonzero(file[dataset].currentData)[0][2]] / (float(mass_entry.get()) * nominal_capacity/1000))
                        file[dataset].recalculate(active_mass)

        elif selectedEntryMode.get() == 'Enter Mass Manually:':
            for dataset in range(num_datasets):
                active_mass = float(mass_entry.get()) / 1000  # assume entry in mg
                batteryData[dataset].recalculate(active_mass)
        for file in combined_bdms_files:
            for dataset in range(len(file)):
                dataSets[combined_bdms_files.index(file)][dataset]['Specific Capacity'] = specificCapacity(file[dataset].cyclenumbers,
                                                                          file[dataset].currentData,file[dataset].speCapData)
                dataSets[combined_bdms_files.index(file)][dataset]['Coulombic Efficiency'] = specificCapacity(file[dataset].cyclenumbers,
                                                                          file[dataset].currentData,
                                                                          file[dataset].speCapData)
                dataSets[combined_bdms_files.index(file)][dataset]['Mean Voltage'] = meanVoltage(file[dataset].cyclenumbers,file[dataset].currentData,file[dataset].voltageData)
                #[combined_bdms_files.index(file)][dataset]['Voltage Curve'] = voltageCurve(3, combined_bdms_files[combined_bdms_files.index(file)][dataset].cyclenumbers,
                 #                                                 combined_bdms_files[combined_bdms_files.index(file)][dataset].speCapData,
                  #                                                combined_bdms_files[combined_bdms_files.index(file)][dataset].voltageData)
             #   dataSets[combined_bdms_files.index(file)][file][dataset]['dQ/dV curve'] = dQdVcurve(3, combined_bdms_files[combined_bdms_files.index(file)][dataset].cyclenumbers,combined_bdms_files[combined_bdms_files.index(file)][dataset].speCapData,combined_bdms_files[combined_bdms_files.index(file)][dataset].voltageData)

    plotfig = plt.figure(figsize=(7, 5), dpi=100)
    x_axis = set_domain.get().split(',')
    y_axis = set_range.get().split(',')

    global pane1
    pane1 = plotfig.add_subplot(1, 1, 1)
    datasetName = selectedData.get()
    colors = [(0, 0, 0), (0.5, 0, 0), (0, 0.5, 0), (0, 0, 0.5), (0.5, 0.5, 0), (0, 0.5, 0.5),
              (0.5, 0, 0.5)]
    counter = 7
    if datasetName == "Specific Capacity":
        #if is_bdms:
        for file in combined_bdms_files:
            for dataset in range(len(file)):
                if dataset_selection[combined_bdms_files.index(file)][dataset].get():
                    counter = plotSpecCapCurves(is_bdms, combined_bdms_files.index(file), dataset,colors, datasetName,counter, batteryData, pane1, displayLegend, dataSets)
            #else:
             #   dataset = 0
              #  counter = plotSpecCapCurves(is_bdms, combined_bdms_files.index(file), dataset, colors, datasetName, counter, batteryData, pane1, displayLegend,
                                       #     dataSets)


     #   if len(combined_bdms_files) == 0:
      #      if batteryData[0].sysFormat == 'Arbin':
       #         for dataset in range(num_datasets):
        #            counter = plotSpecCapCurves(dataset,colors, datasetName,counter, batteryData, pane1, displayLegend, dataSets)
         #   # apply default format settings for specific capacity plot
          #  else:
           #     dataset = 0
            #    counter = plotSpecCapCurves(dataset,colors, datasetName,counter, batteryData, pane1, displayLegend, dataSets)
        #else:
         #   for file in combined_bdms_files:
          #      for dataset in range(len(file)):
           #         counter = plotSpecCapCurves(dataset, colors, datasetName, counter, batteryData, pane1,
            #                                    displayLegend, dataSets)
        pane1.set_xlabel('Cycle Number', fontname = font, fontsize=axesSize)
        pane1.set_ylabel('Specific Discharge Capacity (mAh g'+'\u207b'+'\u00b9'+')', fontname=font, fontsize=axesSize)
        pane1.set_title('Specific Capacity',fontname = font, fontsize = titleSize)
        set_axes(x_axis, y_axis)

    if datasetName == "Coulombic Efficiency":
        #if is_bdms:
        for file in combined_bdms_files:
            if batteryData[0].sysFormat == 'Arbin':
                for dataset in range(len(file)):
                    if dataset_selection[combined_bdms_files.index(file)][dataset].get():
                        counter = plotCoulombicEfficiencyCurves(is_bdms, combined_bdms_files.index(file),dataset,colors, datasetName,counter, batteryData, pane1, displayLegend, dataSets)
            else:
                dataset = 0
                if dataset_selection[combined_bdms_files.index(file)][dataset].get():
                    counter = plotCoulombicEfficiencyCurves(is_bdms, combined_bdms_files.index(file),dataset, colors, datasetName, counter, batteryData, pane1,displayLegend, dataSets)


        pane1.set_xlabel('Cycle Number', fontname = font, fontsize=axesSize)
        pane1.set_ylabel('Coulombic Efficiency', fontname=font, fontsize=axesSize)
        pane1.set_title('Coulombic Efficiency',fontname = font, fontsize = titleSize)
        set_axes(x_axis, y_axis)


    elif datasetName == "Mean Voltage":
        #if is_bdms:
        for file in combined_bdms_files:
            if batteryData[0].sysFormat == 'Arbin':
                for dataset in range(len(file)):
                    if dataset_selection[combined_bdms_files.index(file)][dataset].get():
                        counter = plotMeanVoltageCurves(is_bdms,combined_bdms_files.index(file),dataset, colors, datasetName, counter, batteryData, pane1, displayLegend, dataSets)
            else:
                dataset = 0
                if dataset_selection[combined_bdms_files.index(file)][dataset].get():
                    counter = plotMeanVoltageCurves(is_bdms,combined_bdms_files.index(file),dataset, colors, datasetName, counter, batteryData, pane1,displayLegend, dataSets)


        #pane1.plot(dataSets.get(datasetName)[0],dataSets.get(datasetName)[1],'o',c=[0,0,0])
        #pane1.plot(dataSets.get(datasetName)[0],dataSets.get(datasetName)[2],'*',c=[0,0,0])
        pane1.set_xlabel('Cycle Number',fontname=font,fontsize=axesSize)
        pane1.set_ylabel('Mean Voltage (V)',fontname=font,fontsize=axesSize)
        pane1.set_title('Mean Voltage', fontname=font, fontsize=titleSize)
        set_axes(x_axis, y_axis)

    elif datasetName == "Voltage Curve":
        cycle_numbers = ValidateCycleInput(set_cycle_numbers)

        #if is_bdms:
        for file in combined_bdms_files:
            if batteryData[0].sysFormat == 'Arbin':
                for dataset in range(len(file)):
                    if dataset_selection[combined_bdms_files.index(file)][dataset].get():
                        counter = plotVoltCurves(is_bdms,combined_bdms_files,combined_bdms_files.index(file),cycle_numbers, dataset, dataSets,colors,datasetName,counter, batteryData, pane1, displayLegend)
            else:
                dataset = 0
                if dataset_selection[combined_bdms_files.index(file)][dataset].get():
                    counter = plotVoltCurves(is_bdms,combined_bdms_files,combined_bdms_files.index(file),cycle_numbers, dataset, dataSets, colors, datasetName, counter, batteryData, pane1, displayLegend)

		#Step 1: validate input (a comma-separated list of integers is an acceptable input)
		#Step 2: convert string input to a list (e.g. numpy array) of cycle numbers to be plotted
		#Step 3: obtain dataset for each cycle specified and add to plot
        #symbols = ['o', '*', '.']
        pane1.set_xlabel('Specific Capacity (mAh g'+'\u207b'+'\u00b9'+')',fontname=font,fontsize=axesSize)
        pane1.set_ylabel('Voltage (V)',fontname=font,fontsize=axesSize)
        pane1.set_title('Voltage', fontname=font, fontsize=titleSize)
        set_axes(x_axis, y_axis)



    elif datasetName == "dQ/dV curve":
        cycle_numbers = ValidateCycleInput(set_cycle_numbers)
        #if is_bdms:
        for file in combined_bdms_files:
            if batteryData[0].sysFormat == 'Arbin':
                for dataset in range(len(file)):
                    if dataset_selection[combined_bdms_files.index(file)][dataset].get():
                        counter = plotdQdVCurves(is_bdms,combined_bdms_files,combined_bdms_files.index(file),cycle_numbers, dataset, dataSets, colors, datasetName, counter, batteryData, pane1, displayLegend)
            else:
                dataset = 0
                if dataset_selection[combined_bdms_files.index(file)][dataset].get():
                    counter = plotdQdVCurves(is_bdms,combined_bdms_files,combined_bdms_files.index(file),cycle_numbers, dataset, dataSets, colors, datasetName, counter, batteryData, pane1, displayLegend)

        pane1.set_xlabel('Voltage (V)', fontname=font, fontsize=axesSize)
        pane1.set_ylabel('dQ/dV (mAh g' +'\u207b'+'\u00b9'+ 'V'+'\u207b'+'\u00b9'+')', fontname=font, fontsize=axesSize)
        pane1.set_title('dQ/dV', fontname=font, fontsize=titleSize)
        set_axes(x_axis, y_axis)

    displayTicks(tickSize)
    canvas = FigureCanvasTkAgg(plotfig,master = main_window)
    canvas.draw()
    canvas.get_tk_widget().grid(column = 1, row = 1, columnspan = 2, rowspan = 2)
    selectFolderButton['state'] = tk.NORMAL
	
def importDataFile():
    global batteryData
    global dataSets
    global num_datasets
    global data_selected
    global data_selection_tabs
    global dataset_selection
    global dataset_checkboxes
    global infile_name
    global combined_bdms_files
    global is_bdms
    if not is_bdms:
        while True:
            try: #added try/except in case user cancels file input
                infile_name = tk.filedialog.askopenfile().name
                import_control = tk.Label(init_import_tab, text=infile_name[-20:], bg="#cfe2f3")
                import_control.grid(column=1, row=1, columnspan=2, padx=5, pady=5)
                batteryData = file2dataset(infile_name)
                break
            except:
                print("No file provided")
                return
    else:
        while True:
            try:
                import_control = tk.Label(open_saved_bdms, text=infile_name[-20:], bg="#ffffe3")
                import_control.grid(column=1, row=1, padx=5, pady=5)
                break
            except:
                print("No file provided")
                return
    data_selection_tabs.append(ttk.Frame(DS_Tab_Control)) #add ui tabs for imported dataset
    dataset_selection.append(np.zeros(len(batteryData)).tolist())
    dataset_checkboxes.append(np.zeros(len(batteryData)).tolist())
    DS_Tab_Control.add(data_selection_tabs[-1], text=infile_name[-20:])
    for index in range(len(batteryData)):
        dataset_selection[-1][index] = tk.BooleanVar()
        dataset_checkboxes[-1][index] = tk.Checkbutton(data_selection_tabs[-1], text='Cell ' + str(index + 1), variable = dataset_selection[-1][index], onvalue=True,
                                         offvalue=False)
        dataset_checkboxes[-1][index].grid(column = 1, columnspan = 3, row = index + 1, rowspan = 1, padx=5, pady=5)

    combined_bdms_files.append(batteryData)
    dataSets = []
    for file in combined_bdms_files:
        dataSets.append([])
        for dataset in file:
            dataSets[combined_bdms_files.index(file)].append({})
    if not isinstance(batteryData, list):
        Format = batteryData.sysFormat

    else:  # list type dataset from arbin
        Format = batteryData[0].sysFormat
        num_datasets = len(batteryData)
        mass_entry['state'] = tk.NORMAL
    if batteryData[0].sysFormat == 'Arbin':
        set_nominal_capacity['state'] = tk.NORMAL
        set_nominal_capacity.delete(0, tk.END)
        set_nominal_capacity.insert(0, "180")
    else:
        set_nominal_capacity.delete(0, tk.END)
        set_nominal_capacity.insert(0, "180")
        set_nominal_capacity['state'] = tk.DISABLED


    print('Detected %s file format' % Format)
    print('%d dataset(s) imported' % num_datasets)
    plotDataSetButton['state'] = tk.NORMAL
    bdms_filename_entry['state'] = tk.NORMAL
    bdms_filename_entry.insert(0, infile_name)
    save_bdms_file_button['state'] = tk.NORMAL
    data_selected = True
    is_bdms = False
    return batteryData

def BDMSfile():
    global is_bdms
    global infile_name, infile_counter
    global batteryData
    while True:
        try:
            infile_name = tk.filedialog.askopenfile().name
            break
        except:
            print("No file provided")
            return
    is_bdms = True
    with open(infile_name, 'rb') as dataSetFile:  # load the saved data back in as a batteryDataSet class object
        batteryData = load(dataSetFile)
    batteryData = importDataFile()
    return batteryData

def onSelectData(self):
    if (selectedData.get() == 'Voltage Curve' or selectedData.get() == 'dQ/dV curve') and data_selected == True:
        set_cycle_numbers['state'] = tk.NORMAL
        findMaxCycle()
        message = "Max Cycles: "  + str(findMaxCycle())
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
    elif selectedEntryMode.get() == 'Calculate (enter initial C-rate):':
        # theor_capac_entry['state'] = tk.NORMAL
        mass_entry.delete(0, tk.END)
        mass_entry.insert(0, '0.1')
        # make prompts & extra textbox active

def displayLegend():
    if legend_on.get():
        pane1.legend(prop={'size': legendSize})

def displayTicks(tickSize):
    if toptick_on.get():
        pane1.xaxis.set_tick_params(top=True, direction="in")
        plt.xticks(fontsize=tickSize)
    else:
        pane1.xaxis.set_tick_params(top=False, direction="in")
        plt.xticks(fontsize=tickSize)
    if righttick_on.get():
        pane1.yaxis.set_tick_params(right=True, direction="in")
        plt.yticks(fontsize=tickSize)
    else:
        pane1.yaxis.set_tick_params(right=False, direction="in")
        plt.yticks(fontsize=tickSize)

def findMaxCycle():
    max_cycle_list = []
    if batteryData[0].sysFormat == 'Arbin':
        for dataset in range(num_datasets):
            max_cycle = max(batteryData[dataset].cyclenumbers)
            max_cycle_list.append(int(max_cycle))
    else:
        max_cycle = max(batteryData[0].cyclenumbers)
        max_cycle_list.append(int(max_cycle))
    return max_cycle_list

def set_axes(x_axis, y_axis):
    try:
        for i in range(len(x_axis)):
            x_axis[i] = float(x_axis[i])
        plt.xlim(x_axis)
    except:
        pass
    try:
        for i in range(len(y_axis)):
            y_axis[i] = float(y_axis[i])
        plt.ylim(y_axis)
    except:
        if selectedData.get() == 'dQ/dV curve':
            plt.ylim([-1000,1000])

def selectFolder():
    global folder_name
    folder_name = tk.filedialog.askdirectory()
    save_figure_button['state'] = tk.NORMAL
    folder_control = tk.Label(saveImageFrame, text=folder_name[-20:], bg="#e7fcde")
    folder_control.grid(column=3, row=2, columnspan=2, padx=5, pady=5)

def saveFigure():
    filename = figure_filename_entry.get()
    plt.savefig(str(folder_name) + '/' + filename + '.png')
    return

def chooseFont():
    global font
    font = str(fontEntryMode.get())
    mpl.rc('font', family=font) #https://stackoverflow.com/questions/21933187/how-to-change-legend-fontname-in-matplotlib
    return font

def fontScale(title_font_size_scale, axes_font_size_scale, legend_font_size_scale, ticks_font_size_scale):
    global titleSize, axesSize, legendSize, tickSize
    titleSize = int(title_font_size_scale.get())
    axesSize = int(axes_font_size_scale.get())
    legendSize = int(legend_font_size_scale.get())
    tickSize = int(ticks_font_size_scale.get())
    return titleSize, axesSize, legendSize, tickSize

def ValidateCycleInput(set_cyle_numbers):
    cycle_numbers_string = set_cycle_numbers.get()  # retrieve user input providing cycle numbers
    # convert string input to list of integers
    cycle_numbers_strings = cycle_numbers_string.split(",")
    cycle_numbers = []
    for cycle in cycle_numbers_strings:
        try:
            cycle_numbers.append(int(cycle))
        except:
            print("Please enter valid input. This is a list of comma separated integers.")
    return cycle_numbers


def saveBDMSFile():
    global batteryData
    with open(bdms_filename_entry.get(), 'wb') as dataSetFile:  # save the batteryDataSet class object(s) to a file
        dump(batteryData, dataSetFile)
    return batteryData, dataSetFile

main_window = tk.Tk()
main_window.title('Battery Data Manager')
screen_size = [main_window.winfo_screenwidth(),main_window.winfo_screenheight()]
main_window.geometry("%ix%i" %(screen_size[0]*3/4,screen_size[1]*3/4))

#control frame
controlframe = tk.Frame(main_window,bg="#0b60ad")
controlframe.grid(column = 0, row = 0, padx = 10, pady = 10, ipadx = 10, ipady = 10)

CF_Tab_Control = ttk.Notebook(controlframe)
init_import_tab = ttk.Frame(CF_Tab_Control)
open_saved_bdms = ttk.Frame(CF_Tab_Control)
CF_Tab_Control.add(init_import_tab,text = "Initial Excel File Import")
CF_Tab_Control.add(open_saved_bdms,text = "Open Saved BDMS File")
CF_Tab_Control.grid(column = 0, row = 3, columnspan = 3 , rowspan = 3, padx = 5, pady = 5)

import_control = tk.Label(controlframe,text = "File and Dataset Control", bg = "#9fc5e8")
import_control.grid(column = 0, row = 0, columnspan = 2, padx = 5, pady = 5)

plotDataSetButton = tk.Button(controlframe,command = show_plot,state=tk.DISABLED)
plotDataSetButton['text'] = 'Plot Data'
plotDataSetButton.grid(column = 0,row = 1,padx = 5, pady = 5)

addDataFileButton = tk.Button(init_import_tab,command = importDataFile)
addDataFileButton['text'] = 'Select Excel File'
addDataFileButton.grid(column = 0,row = 1,padx = 5,pady = 5)
#addDataFileButton.place(relx = 0.1, rely = 0.2, anchor = 'center')

selectedEntryMode = tk.StringVar(main_window)
selectedEntryMode.set('Calculate (enter initial C-rate):')
mass_entry_mode = tk.OptionMenu(init_import_tab, selectedEntryMode, 'Enter Mass Manually:', 'Calculate (enter initial C-rate):',
                                command=onSelectEntryMode)
mass_entry_mode.grid(column = 0,row = 2, padx = 5, pady = 5)
#mass_entry_mode.place(relx=0.15, rely=0.4, anchor='center')
mass_entry_mode.config(width=25)
mass_entry = tk.Entry(init_import_tab)
mass_entry.insert(0,"Initial C-rate")
mass_entry.grid(column = 1, row = 2, padx = 5, pady = 5)

selectedData = tk.StringVar(main_window) #the selected string from the dropdown list will be stored in this variable
selectedData.set('Specific Capacity') #this is the default dataset
dataSelect = tk.OptionMenu(controlframe, selectedData, 'Specific Capacity', 'Coulombic Efficiency', 'Mean Voltage', 'Voltage Curve', 'dQ/dV curve',command = onSelectData)
dataSelect.grid(column = 0, row = 2, padx = 5, pady = 5)
#dataSelect.place(relx = 0.1, rely = 0.3, anchor = 'center')
dataSelect.config(width = 15)

set_cycle_numbers = tk.Entry(controlframe, state = tk.DISABLED)
set_cycle_numbers.insert(0,"Cycle number(s):")
set_cycle_numbers.grid(column = 1,row = 2)

#formatframe
formatFrame = tk.Frame(main_window, bg = "#674ea7")
formatFrame.grid(column = 0, row = 1, padx = 10, pady = 10, ipadx = 10, ipady = 10)

graph_control = tk.Label(formatFrame,text = "Graph Control", bg = "#b4a7d6")
graph_control.grid(column = 0, row = 0, columnspan = 2, padx = 5, pady = 5)

legend_on = tk.BooleanVar()
legend_checkbox = tk.Checkbutton(formatFrame, text='Display Legend', variable=legend_on, onvalue=True, offvalue=False, command=displayLegend, bg="#e9e0ff")
legend_checkbox.grid(column=0, row=10, columnspan = 2, padx=5, pady=5)

toptick_on = tk.BooleanVar()
toptick_checkbox = tk.Checkbutton(formatFrame, text='Top Ticks', variable=toptick_on, onvalue=True, offvalue=False, command=displayTicks, bg="#e9e0ff")
toptick_checkbox.grid(column=0, row=9, padx=5, pady=5)

righttick_on = tk.BooleanVar()
righttick_checkbox = tk.Checkbutton(formatFrame, text='Right Ticks', variable=righttick_on, onvalue=True, offvalue=False, command=displayTicks, bg="#e9e0ff")
righttick_checkbox.grid(column=1, row=9, padx=5, pady=5)

#toplabel_on = tk.BooleanVar()
#toplabel_checkbox = tk.Checkbutton(formatFrame, text='Top Labels', variable=toplabel_on, onvalue=True, offvalue=False, command=displayTicks, bg="#e9e0ff")
#toplabel_checkbox.grid(column=0, row=9, padx=5, pady=5)

#rightlabel_on = tk.BooleanVar()
#rightlabel_checkbox = tk.Checkbutton(formatFrame, text='Right Labels', variable=rightlabel_on, onvalue=True, offvalue=False, command=displayTicks, bg="#e9e0ff")
#rightlabel_checkbox.grid(column=1, row=9, padx=5, pady=5)

#font_control = tk.Label(formatFrame,text = "Font", bg = "#e9e0ff", width = 5)
#font_control.grid(column = 0, row = 4, padx = 5, pady = 5)

font_control = tk.Label(formatFrame,text = "Font Style", bg = "#e9e0ff", width = 10)
font_control.grid(column = 0, row = 4,padx = 5, pady = 5)

fontEntryMode = tk.StringVar(main_window)
fontEntryMode.set('Arial')
font_selected = tk.OptionMenu(formatFrame, fontEntryMode, 'Arial', 'Times New Roman', 'Calibri','Helvetica', 'Serif', 'Algerian', 'Wingdings', command=chooseFont)
font_selected.grid(column = 1,row = 4,  padx = 6, pady = 5)

domain_control = tk.Label(formatFrame,text = "Domain ", bg = "#e9e0ff", width = 15)
domain_control.grid(column = 0, row = 2, padx = 5, pady = 5)
set_domain = tk.Entry(formatFrame)
set_domain.insert(0,"Min, Max")
set_domain.grid(column = 1,row = 2)

range_control = tk.Label(formatFrame,text = " Range ", bg = "#e9e0ff", width = 10)
range_control.grid(column = 0, row = 3, padx = 5, pady = 5)
set_range = tk.Entry(formatFrame)
set_range.insert(0,"Min, Max")
set_range.grid(column = 1,row = 3)

nominal_capacity_control = tk.Label(formatFrame,text = 'Nominal Capacity (mAh g'+'\u207b'+'\u00b9'+')', bg = "#e9e0ff")
nominal_capacity_control.grid(column = 0, row = 1, padx = 5, pady = 5)
set_nominal_capacity = tk.Entry(formatFrame,state=tk.DISABLED)
set_nominal_capacity.grid(column = 1,row = 1)

title_font_size = tk.Label(formatFrame, text = "Title Font Size:", bg = "#e9e0ff")
title_font_size.grid(column = 0, row = 5,  padx = 5, pady = 5)

title_font_size_scale = tk.Scale(formatFrame, from_ = 1, to_ = 20, orient = 'horizontal')
title_font_size_scale.grid(column = 0, row = 6,  padx = 5, pady = 5)
title_font_size_scale.set(15)

axes_font_size = tk.Label(formatFrame, text = "Axes Font Size:", bg = "#e9e0ff")
axes_font_size.grid(column = 1, row = 5,  padx = 5, pady = 5)

axes_font_size_scale = tk.Scale(formatFrame, from_ = 1, to_ = 20, orient = 'horizontal')
axes_font_size_scale.grid(column = 1, row = 6,  padx = 5, pady = 5)
axes_font_size_scale.set(14)

legend_font_size = tk.Label(formatFrame, text = "Legend Font Size:", bg = "#e9e0ff")
legend_font_size.grid(column = 0, row = 7,  padx = 5, pady = 5)

legend_font_size_scale = tk.Scale(formatFrame, from_ = 1, to_ = 20, orient = 'horizontal')
legend_font_size_scale.grid(column = 0, row = 8,  padx = 5, pady = 5)
legend_font_size_scale.set(12)

ticks_font_size = tk.Label(formatFrame, text = "Ticks Font Size:", bg = "#e9e0ff")
ticks_font_size.grid(column = 1, row = 7,  padx = 5, pady = 5)

ticks_font_size_scale = tk.Scale(formatFrame, from_ = 1, to_ = 20, orient = 'horizontal')
ticks_font_size_scale.grid(column = 1, row = 8,  padx = 5, pady = 5)
ticks_font_size_scale.set(14)

saveImageFrame = tk.Frame(main_window, bg = "#00b809")
saveImageFrame.grid(column = 1, row = 0, padx = 10, pady = 10, ipadx = 10, ipady = 10)

SIF_Tab_Control = ttk.Notebook(saveImageFrame)
saveImageTab = ttk.Frame(SIF_Tab_Control)
saveFileTab = ttk.Frame(SIF_Tab_Control)
SIF_Tab_Control.add(saveImageTab,text = "Save Image")
SIF_Tab_Control.add(saveFileTab,text = "Save File")
SIF_Tab_Control.grid(column = 2, row = 1, columnspan = 3 , rowspan = 3, padx = 5, pady = 5)

general_save_control = tk.Label(saveImageFrame,text = "Save Figures and Datasets", bg = "#a5f584")
general_save_control.grid(column = 2, row = 0, columnspan = 3, rowspan = 1, padx = 5, pady = 5)

save_bdms_file_button = tk.Button(saveFileTab,command = saveBDMSFile, state = tk.DISABLED)
save_bdms_file_button['text'] = 'Save BDMS File'
save_bdms_file_button.grid(column = 0, row = 3, columnspan = 2, padx = 5, pady = 5)

bdms_file_save_control = tk.Label(saveFileTab,text = "File Name")
bdms_file_save_control.grid(column = 0, row = 2, padx = 5, pady = 5)

bdms_filename_entry = tk.Entry(saveFileTab, state=tk.DISABLED)
bdms_filename_entry.grid(column = 1,row = 2, padx = 5, pady = 5)

save_figure_button = tk.Button(saveImageTab,command = saveFigure, state = tk.DISABLED)
save_figure_button['text'] = 'Save Figure'
save_figure_button.grid(column = 2, row = 3, padx = 5, pady = 5)

figure_filename_entry = tk.Entry(saveImageTab)
figure_filename_entry.insert(0,'Figure Filename')
figure_filename_entry.grid(column = 3,row = 3, padx = 5, pady = 5)

selectFolderButton = tk.Button(saveImageTab,command = selectFolder, state = tk.DISABLED)
selectFolderButton['text'] = 'Select Folder'
selectFolderButton.grid(column = 2, row = 2, padx = 5, pady = 5)

selectDataFrame = tk.Frame(main_window, bg = "#FFFF00")
selectDataFrame.grid(column = 2, row = 0, padx = 10, pady = 10, ipadx = 10, ipady = 10)

DS_Tab_Control = ttk.Notebook(selectDataFrame)
DS_Tab_Control.grid(column = 0, row = 1, rowspan = 5, columnspan = 3, padx = 5, pady = 5)

bdms_control = tk.Label(selectDataFrame,text = "Data To Be Displayed", bg="#ffffa3")
bdms_control.grid(column = 0, row = 0, columnspan = 2, padx = 5, pady = 5)

addBDMSDataFileButton = tk.Button(open_saved_bdms,command = BDMSfile)
addBDMSDataFileButton['text'] = 'Select Data File'
addBDMSDataFileButton.grid(column = 0,row = 1,padx = 5,pady = 5)

main_window.mainloop() #keep window open until closed by user