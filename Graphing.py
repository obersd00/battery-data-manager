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

def plotSpecCapCurves(dataset,colors, datasetName,counter, batteryData, pane1, displayLegend, dataSets):
    c = counter % 7
    dataset_label = 'Cell ' + str(int(dataset + 1))
    pane1.plot(dataSets[dataset].get(datasetName)[0], dataSets[dataset].get(datasetName)[1], '.', c=colors[c],
               label=dataset_label)
    displayLegend()
    counter += 1
    return counter

def plotMeanVoltageCurves(dataset, colors, datasetName, counter, batteryData, pane1, displayLegend, dataSets):
    c = counter % 7
    dataset_label = 'Cell ' + str(int(dataset) + 1)
    pane1.plot(dataSets[dataset].get(datasetName)[0], dataSets[dataset].get(datasetName)[1], '.', c=colors[c],
               label=dataset_label)
    counter += 1
    displayLegend()
    return counter

def plotVoltCurves(cycle_numbers, dataset, dataSets,colors, datasetName,counter, batteryData, pane1, displayLegend):
    for i in range(len(cycle_numbers)):
        c = counter % 7
        cycle_label = 'Cell ' + str(int(dataset + 1)) + ' Cycle ' + str(cycle_numbers[i])  # generates cycle label as neccessary
        dataSets[dataset]['Voltage Curve'] = voltageCurve(cycle_numbers[i], batteryData[dataset].cyclenumbers, batteryData[dataset].speCapData, batteryData[dataset].voltageData)
        pane1.plot(dataSets[dataset].get(datasetName)[0].squeeze(), dataSets[dataset].get(datasetName)[1].squeeze(), '.', c=colors[c], label=cycle_label)  # check if adding to data on plot or overwriting previous
        counter += 1
        displayLegend()
    return counter

def plotdQdVCurves(cycle_numbers, dataset, dataSets, colors, datasetName, counter, batteryData, pane1, displayLegend):
    for i in range(len(cycle_numbers)):
        # s = counter % 3
        c = counter % 7
        cycle_label = 'Cell ' + str(int(dataset + 1)) + ' Cycle ' + str(cycle_numbers[i])
        dataSets[dataset]['dQ/dV curve'] = dQdVcurve(cycle_numbers[i], batteryData[dataset].cyclenumbers, batteryData[dataset].speCapData,batteryData[dataset].voltageData)
        pane1.plot(dataSets[dataset].get(datasetName)[0], dataSets[dataset].get(datasetName)[1], '.', c=colors[c],label=cycle_label)
        counter += 1
        displayLegend()
    return counter

