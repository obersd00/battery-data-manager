from batteryDataSet import batteryDataSet
import numpy as np


#this script contains functions to process raw data and output vectors of (x,y) coordinates for plotting


def specificCapacity(cycleNumberData,speCapData):
    return

def meanVoltage(cycleNumberData,currentData,voltageData):
    num_cycles = int(np.amax(cycleNumberData))
    meanVoltageData = np.empty([num_cycles-1,3])
    for cycnum in range(1,num_cycles-1): #ignore last cycle as incomplete dataset may cause parsing errors
        cycle_indices = np.where(cycleNumberData==cycnum)[0]
        cycle_charge_indices = np.array([index for index in cycle_indices if currentData[index] > 0]) 
        cycle_discharge_indices = np.array([index for index in cycle_indices if currentData[index] < 0])
        cycle_charge_voltage_data = [voltageData[index] for index in cycle_charge_indices]
        cycle_discharge_voltage_data = [voltageData[index] for index in cycle_discharge_indices]
        mean_charge_voltage = np.average(cycle_charge_voltage_data)
        mean_discharge_voltage = np.average(cycle_discharge_voltage_data)
        voltage_hysteresis = mean_charge_voltage - mean_discharge_voltage
        meanVoltageData[cycnum] = [mean_charge_voltage,mean_discharge_voltage,voltage_hysteresis]
    return meanVoltageData

def voltageCurve(cycleNumber,cycleNumberData,speCapData,voltageData):
    return

def dQdVcurve(cycleNumber,cycleNumberData,speCapData,voltageData):
    return


