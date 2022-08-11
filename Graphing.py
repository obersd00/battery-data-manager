import matplotlib.pyplot as plt  # testing file edit
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import xlrd2  # the og xlrd doesn't support .xlsx files but this one is more actively maintained
import os  # to check directory
import numpy as np
import tkinter as tk
from file2dataset import file2dataset
from dataProcesses import *
import matplotlib as mpl

global x
x=7

def plotSpecCapCurves(is_bdms,file,dataset,colors, datasetName,counter, batteryData, pane1, displayLegend, dataSets):
    c = counter % 7
    dataset_label = 'File ' + str(int(file+1)) + ' Cell ' + str(int(dataset + 1))
    pane1.plot(dataSets[file][dataset].get(datasetName)[0], dataSets[file][dataset].get(datasetName)[1], '.', c=colors[c],label=dataset_label)
    displayLegend()
    counter += 1
    return counter

def plotCoulombicEfficiencyCurves(is_bdms,file,dataset,colors, datasetName,counter, batteryData, pane1, displayLegend, dataSets):
    c = counter % 7
    dataset_label = 'File ' + str(int(file+1)) + ' Cell ' + str(int(dataset + 1))
    pane1.plot(dataSets[file][dataset].get(datasetName)[0], dataSets[file][dataset].get(datasetName)[3], '.', c=colors[c],
               label=dataset_label)
    displayLegend()
    counter += 1
    return counter

def plotMeanVoltageCurves(is_bdms,file,dataset, colors, datasetName, counter, batteryData, pane1, displayLegend, dataSets):
    c = counter % 7
    dataset_label = 'File ' + str(int(file+1)) + ' Cell ' + str(int(dataset) + 1)
    pane1.plot(dataSets[file][dataset].get(datasetName)[0], dataSets[file][dataset].get(datasetName)[1], '.', c=colors[c],
               label=dataset_label)
    counter += 1
    displayLegend()
    return counter

def plotVoltCurves(is_bdms,combined_bdms_files, file,cycle_numbers, dataset, dataSets,colors, datasetName,counter, batteryData, pane1, displayLegend):
    for i in range(len(cycle_numbers)):
        c = counter % 7
        cycle_label = 'File ' + str(int(file+1)) + ' Cell ' + str(int(dataset + 1)) + ' Cycle ' + str(cycle_numbers[i])  # generates cycle label as neccessary
        print('see this', file)
        #if is_bdms:
        dataSets[file][dataset]['Voltage Curve'] = voltageCurve(cycle_numbers[i], combined_bdms_files[file][dataset].cyclenumbers, combined_bdms_files[file][dataset].speCapData, combined_bdms_files[file][dataset].voltageData)
        #else:
         #   dataSets[dataset]['Voltage Curve'] = voltageCurve(cycle_numbers[i], batteryData[dataset].cyclenumbers,
            #                                                  batteryData[dataset].speCapData,
             #                                                 batteryData[dataset].voltageData)

        pane1.plot(dataSets[file][dataset].get(datasetName)[0].squeeze(), dataSets[file][dataset].get(datasetName)[1].squeeze(), '.', c=colors[c], label=cycle_label)  # check if adding to data on plot or overwriting previous
        counter += 1
        displayLegend()
    return counter

def plotdQdVCurves(is_bdms,combined_bdms_files, file, cycle_numbers,dataset, dataSets, colors, datasetName, counter, batteryData, pane1, displayLegend):
    for i in range(len(cycle_numbers)):
        # s = counter % 3
        c = counter % 7
        cycle_label = 'File ' + str(int(file+1)) + ' Cell ' + str(int(dataset + 1)) + ' Cycle ' + str(cycle_numbers[i])
        #if is_bdms:
        dataSets[file][dataset]['dQ/dV curve'] = dQdVcurve(cycle_numbers[i], combined_bdms_files[file][dataset].cyclenumbers, combined_bdms_files[file][dataset].speCapData,combined_bdms_files[file][dataset].voltageData)
        #else:
         #   dataSets[dataset]['dQ/dV curve'] = dQdVcurve(cycle_numbers[i], batteryData[dataset].cyclenumbers,
          #                                               batteryData[dataset].speCapData,
           #                                              batteryData[dataset].voltageData)
        pane1.plot(dataSets[file][dataset].get(datasetName)[0], dataSets[file][dataset].get(datasetName)[1], '.', c=colors[c],label=cycle_label)
        counter += 1
        displayLegend()
    return counter

