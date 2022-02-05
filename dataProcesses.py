from batteryDataSet import batteryDataSet
import numpy as np


#this script contains functions to process raw data and output vectors of (x,y) coordinates for plotting


def specificCapacity(cycleNumberData,currentData,speCapData): #outputs specific charge/discharge capacity as fcn of cycle number
    num_cycles = int(np.amax(cycleNumberData))
    specificCapacityData = np.empty([num_cycles-1, 4])
    for cycnum in range(1, num_cycles):
        cycle_indices = np.where(cycleNumberData==cycnum)[0]
        cycle_charge_indices = np.array([index for index in cycle_indices if currentData[index] > 0])
        cycle_discharge_indices = np.array([index for index in cycle_indices if currentData[index] < 0])
        charge_capacities = [speCapData[index] for index in cycle_charge_indices]
        cycle_charge_capacity = np.amax(charge_capacities)
        discharge_capacities = [speCapData[index] for index in cycle_discharge_indices]
        cycle_discharge_capacity = np.amax(discharge_capacities)
        cycle_CE = cycle_discharge_capacity/cycle_charge_capacity
        specificCapacityData[cycnum-1] = [cycnum, cycle_charge_capacity, cycle_discharge_capacity,cycle_CE]
    return specificCapacityData.transpose()

def meanVoltage(cycleNumberData,currentData,voltageData): #outputs mean charge/discharge voltage & hysteresis as fcn of cycle number
    num_cycles = int(np.amax(cycleNumberData))
    meanVoltageData = np.empty([num_cycles-1,4])
    for cycnum in range(1,num_cycles): #ignore last cycle as incomplete dataset may cause parsing errors
        cycle_indices = np.where(cycleNumberData==cycnum)[0] #cycle_indices are indices of raw dataset corresponding to the specified cycle number
        cycle_charge_indices = np.array([index for index in cycle_indices if currentData[index] > 0]) 
        cycle_discharge_indices = np.array([index for index in cycle_indices if currentData[index] < 0])
        cycle_charge_voltage_data = [voltageData[index] for index in cycle_charge_indices]
        cycle_discharge_voltage_data = [voltageData[index] for index in cycle_discharge_indices]
        mean_charge_voltage = np.average(cycle_charge_voltage_data)
        mean_discharge_voltage = np.average(cycle_discharge_voltage_data)
        voltage_hysteresis = mean_charge_voltage - mean_discharge_voltage
        meanVoltageData[cycnum-1] = [cycnum,mean_charge_voltage,mean_discharge_voltage,voltage_hysteresis]
    return meanVoltageData.transpose()

def voltageCurve(cycleNumber,cycleNumberData,speCapData,voltageData): #outputs voltage vs specific capacity for a specified cycle number
    cycle_indices = np.where(cycleNumberData==cycleNumber)
    specific_capacity = np.array([speCapData[index] for index in cycle_indices])
    voltage = np.array([voltageData[index] for index in cycle_indices])
    return [specific_capacity,voltage]

def dQdVcurve(cycleNumber,cycleNumberData,speCapData,voltageData): #outputs differential of specific capacity w.r.t. voltage (dQ/dV) as fcn of voltage for a specified cycle number
    return #[voltage,dqdv]


