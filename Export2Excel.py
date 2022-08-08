import xlwt
from xlwt import Workbook
from dataProcesses import specificCapacity
from batteryDataSet import batteryDataSet
from file2dataset import file2dataset


def createSheet(batteryData, dataSets, specificCapacity, meanVoltage, voltageCurve, dQdVcurve, num_datasets):
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
    wb = Workbook()
    sheet1 = wb.add_sheet('Specific Capacity Data')
    sheet1.write(0, 0, 'Cycle Number')
    sheet1.write(0, 1, 'Cycle Charge Capacity')
    sheet1.write(0, 2, 'Cycle Discharge Capacity')
    sheet1.write(0, 3, 'Cycle CE')
    for dataset in range(num_datasets):
        for j in range(len(dataSets[dataset]['Specific Capacity'])):
            for i in range(len(dataSets[dataset]['Specific Capacity'][j])):
                sheet1.write(i+1, j, dataSets[dataset]['Specific Capacity'][j][i] )

    wb.save('attempt1.xls')