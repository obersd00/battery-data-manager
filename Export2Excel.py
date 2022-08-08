import xlwt
from xlwt import Workbook
from dataProcesses import specificCapacity
from batteryDataSet import batteryDataSet
from file2dataset import file2dataset
global sheets, wb, row1
sheets = []
wb = Workbook()
row1 = ['Cycle Number', 'Cycle Charge Capacity', 'Cycle Discharge Capacity', 'Cycle CE', 'Cycle Number', 'Mean Charge Voltage', 'Mean Discharge Voltage', 'Voltage Hysteresis',  'Voltage', 'dQdV' ]

def createSheet(batteryData, dataSets, specificCapacity, meanVoltage, voltageCurve, dQdVcurve, num_datasets):
    for dataset in range(num_datasets):
        dataSets[dataset]['Specific Capacity'] = specificCapacity(batteryData[dataset].cyclenumbers,
                                                                  batteryData[dataset].currentData,
                                                                  batteryData[dataset].speCapData)
        dataSets[dataset]['Coulombic Efficiency'] = specificCapacity(batteryData[dataset].cyclenumbers,
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
        sheets.append(wb.add_sheet('Dataset ' + str(dataset)))
        for i in range(len(row1)):
            sheets[dataset].write(0, i, row1[i])
        for j in range(len(dataSets[dataset]['Specific Capacity'])):
            for i in range(len(dataSets[dataset]['Specific Capacity'][j])):
                sheets[dataset].write(i+1, j, dataSets[dataset]['Specific Capacity'][j][i] )
        for j in range(len(dataSets[dataset]['Mean Voltage'])):
            for i in range(len(dataSets[dataset]['Mean Voltage'][j])):
                sheets[dataset].write(i+1, j+4, dataSets[dataset]['Mean Voltage'][j][i] )
        for j in range(len(dataSets[dataset]['Voltage Curve'][1])):
            for i in range(len(dataSets[dataset]['Voltage Curve'][1][j])):
            #print(dataSets[dataset]['Voltage Curve'][1][j].squeeze())
            #for i in range(len(dataSets[dataset]['Voltage Curve'][j+1])):
                sheets[dataset].write(i+1, j+8, dataSets[dataset]['Voltage Curve'][1][j][i])
        #for j in range(len(dataSets[dataset]['dQdV Curve'])):
         #   for i in range(len(dataSets[dataset]['dQdV Curve'][j])):
          #      sheets[dataset].write(i+, j+10, dataSets[dataset]['dQdV Curve'][j][i] )

    wb.save('three-quarters dataset.xls')