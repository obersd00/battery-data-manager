
class batteryDataSet:
    'Class to provide consistent format for dataset representations'
    def __init__(self,data_header_dictionary,sysFormat='Arbin'):
        #Integer suffixes are added (e.g. 'Cycle0' instead of 'Cycle' for Land data) to prevent ambiguity about that tab from which they came in the excel file
        import numpy as np
        if sysFormat=='Arbin':
            combined _capacity_data = []
            for i in range(len(data_header_dictionary.get('Charge_Capacity(Ah)')):
                combined_capacity_data[i] = data_header_dictionary.get('Discharge_Capacity(Ah)')[i] if data_header_dictionary.get('Current(A)')[i] < 0 else data_header_dictionary.get('Charge_Capacity(Ah)')
            data_header_dictionary['Discharge_Capacity(Ah)'] = combined_capacity_data
 
        self.cyclenumbers = np.array(data_header_dictionary.get('Cycle_Index')) if sysFormat == 'Arbin' else np.array(data_header_dictionary.get('Cycle-Index2'))
        self.speCapData = np.array(data_header_dictionary.get('Discharge_Capacity(Ah)')) if sysFormat == 'Arbin' else np.array(data_header_dictionary.get('SpeCap/mAh/g2'))
        self.voltageData = voltageData #Arbin: 'Voltage(V)' | Land: 'Voltage/V'
        self.step_index_record = step_index #Arbin:'Step_Index' | Land: 'Step_Index'
        self.cycle_index_record = cycle_index_record #Arbin: 'Cycle_Index' | Land: 'Cycle-Index'
        #self.charge_capacity_stats = charge_capacity_stats #Arbin: 'Charge_Capacity(Ah)' | Land: 'SpeCap/mAh/g'
        #self.discharge_capacity_stats = discharge_capacity_stats #Arbin: 'Discharge_Capacity(Ah)' | Land: 'SpeCap/mAh/g'
        #self.charge_voltage_stats = charge_voltage_stats #Arbin: 'Voltage(V)' | Land: 'MedVoltC/V'
        #self.discharge_voltage_stats = discharge_voltage_stats #Arbin: 'Voltage' | Land: 'MedVoltD/V'
        #self.efficency_stats = efficiency_stats #Land: 'Efficiency/%'
