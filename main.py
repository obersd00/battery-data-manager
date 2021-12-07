import matplotlib.pyplot as plt #testing file edit
import xlrd2 #the og xlrd doesn't support .xlsx files but this one is more actively maintained'
import os #to check directory
import numpy as np

#Landt Format
SHEET_NAMES_LANDT = np.array(['Cycle-Tab','Step-Tab','Record-Tab'])
COL_NAMES_LANDT = np.array([['Cycle','CapC','CapD','SpeCapC','SpeCapD','Efficiency','EnergyC','EnergyD','MedVoltC','MedVoltD','CC-Cap','CC-Perc',\
	'PlatCapD','PlatSpeCapD','PlatPercD','PlatTimeD','CaptnC','CaptnD','rd','rd2','SpeEnergyC','SpeEnergyD','EndVoltD','RetentionD','DCIR_C',\
	'DCIR_D'],\
	['Step','Mode','Period','Capacity','SpeCap','Power','Capacitance','SpeEnergy','MedVolt','StartVolt','EndVolt','','','','','','','','','',
	'','','','','',''],\
	['Record','Test Time',\
	'Current','Capacity','SpeCap','SOC|DOD','Voltage','Energy','SpeEnergy','AuxTemp','AuxVolt','SysTime','[All Auxiliary-Chl]*','Cycle-Index',\
	'Step-Index','Step-State','','','','','','','','','']]) #add empty strings for consistent array dimensions

#Arbin Format
COL_NAMES_ARBIN = np.array(['Data_Point','Test_Time(s)','Date_Time','Step_Time(s)','Step_Index','Cycle_Index','Current(A)','Voltage(V)',\
	'Charge_Capacity(Ah)','Discharge_Capacity(Ah)','Charge_Energy(Wh)','Discharge_Energy(Wh)','dV/dt(V/s)']) #a few other column names but they aren't typically populated

#import N files with electrochemical datasets
total_files = 2
file_names = empty([total_files,2]) #second column to specify number of datasets for each file 

for fn in range(total_files):
		#find number of datasets in file and construct array
		file_names[fn,:] ='ANO Nb doping Data/Half Cell Tests/Temperature Optimization/093_ANO_LNO_700-r2_004_3-1.xlsx'
		

wb = xlrd2.open_workbook(workbook_location)
cyclestats=wb.sheet_by_index(0)
cc = cyclestats.ncols
dataset=np.array([[float(cyclestats.cell_value(row+1,col)) for col in range(cyclestats.ncols)]for row in range(cyclestats.nrows-2)]) #import data from xlsx spreadsheet to np array format
cycnum = dataset[1:cyclestats.nrows-1,0] #account for column titles
spec_caps = dataset[1:cyclestats.nrows-1,2]
fig = plt.figure()
ax = fig.gca()
ax.plot(cycnum,spec_caps,'o',c=[0,0,0])
plt.ylabel('Specific Discharge Capacity (mAh / g)',fontname='Arial',fontsize=20,labelpad=10)
plt.yticks(fontname='Arial',fontsize=12)
plt.xlabel('Cycle Number',fontname='Arial',fontsize=20,labelpad=20)
plt.xticks(fontname='Arial',fontsize=12)
x='[insert dataset name]'
plt.title('Cycle life of %s' %x, fontname='Arial',fontsize=20)
plt.legend(['Im a freaking legend'],loc='lower left',bbox_to_anchor=(0,0,0.5,0.5),borderaxespad=0.5,frameon=False)
ax.spines["top"].set_color([0,0,0])
ax.spines["top"].set_linewidth(3)
ax.spines["bottom"].set_linewidth(3)
ax.spines["left"].set_linewidth(3)
ax.spines["right"].set_linewidth(3)
top_ax = ax.secondary_xaxis("top")
top_ax.tick_params(axis='x',direction='in')
top_ax.set_xticklabels([]) #remove number labels from top axis
top_ax.tick_params(length=15,width=2)
ax.tick_params(axis='x',length=15,width=2,direction='in')
ax.tick_params(axis='y',length=10,width=2,direction='in')
plt.show()
