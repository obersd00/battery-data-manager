import datetime
import numpy as np
class batteryDataSet:
    'Class to provide consistent format for dataset representations'
    def __init__(self,data_header_dictionary,sysFormat='Arbin',active_mass=0.01):
        #Integer suffixes are added (e.g. 'Cycle0' instead of 'Cycle' for Land data) to prevent ambiguity about that tab from which they came in the excel file
        #print(data_header_dictionary)
        self.active_mass = active_mass
        self.sysFormat = sysFormat
        import numpy as np
        if sysFormat=='Arbin':
            combined_capacity_data = np.empty([len(data_header_dictionary.get('Charge_Capacity(Ah)')),1])
            for i in range(len(data_header_dictionary.get('Charge_Capacity(Ah)'))):
                combined_capacity_data[i] = data_header_dictionary.get('Discharge_Capacity(Ah)')[i] if data_header_dictionary.get('Current(A)')[i] < 0 else data_header_dictionary.get('Charge_Capacity(Ah)')[i]
            data_header_dictionary['Discharge_Capacity(Ah)'] = combined_capacity_data/active_mass

        else:
            temp_time_record = data_header_dictionary.get('TestTime2')
            test_time_record = []
            for test_time in temp_time_record:
                if '-' in str(test_time):
                    test_time = test_time.split('-')
                    hours_mins_secs = test_time[1]
                    hours_mins_secs = hours_mins_secs.split(':')
                    test_time = (int(test_time[0]) * 86400) + (int(hours_mins_secs[0]) * 3600) + (
                                int(hours_mins_secs[1]) * 60) + int(hours_mins_secs[2])
                else:
                    test_time = 86400 * float(test_time)
                test_time_record.append(test_time)
        self.data_header_dictionary = data_header_dictionary
        self.cyclenumbers = np.array(data_header_dictionary.get('Cycle_Index')) if sysFormat == 'Arbin' else np.array(data_header_dictionary.get('Cycle-Index2'))
        print(self.cyclenumbers)
        self.speCapData = np.array(data_header_dictionary.get('Discharge_Capacity(Ah)')) if sysFormat == 'Arbin' else np.array(data_header_dictionary.get('SpeCap/mAh/g2'))
        self.voltageData =  np.array(data_header_dictionary.get('Voltage(V)')) if sysFormat == 'Arbin' else np.array(data_header_dictionary.get('Voltage/V2'))
        self.step_index_record = np.array(data_header_dictionary.get('Step_Index')) if sysFormat == 'Arbin' else np.array(data_header_dictionary.get('Step_Index2'))
        self.cycle_index_record = np.array(data_header_dictionary.get('Cycle_Index')) if sysFormat == 'Arbin' else np.array(data_header_dictionary.get('Cycle-Index2'))
        self.test_time_record = np.array(data_header_dictionary.get('Test_Time(s)')) if sysFormat == 'Arbin' else np.array(test_time_record) #np.array(data_header_dictionary.get('TestTime2'))
        self.currentData = np.array(data_header_dictionary.get('Current(A)')) if sysFormat == 'Arbin' else 1e-3*np.array(data_header_dictionary.get('Current/mA2')) 
    #def set_active_mass(self,active_mass):
	    #self.active_mass = active_mass
    def recalculate(self,active_mass):
            if self.sysFormat=='Arbin':
                combined_capacity_data = np.empty([len(self.data_header_dictionary.get('Charge_Capacity(Ah)')),1])
                for i in range(len(self.data_header_dictionary.get('Charge_Capacity(Ah)'))):
                    combined_capacity_data[i] = self.data_header_dictionary.get('Discharge_Capacity(Ah)')[i] if self.data_header_dictionary.get('Current(A)')[i] < 0 else self.data_header_dictionary.get('Charge_Capacity(Ah)')[i]
                self.data_header_dictionary['Discharge_Capacity(Ah)'] = 1000*combined_capacity_data/active_mass
            self.active_mass = active_mass
            self.speCapData = np.array(self.data_header_dictionary.get('Discharge_Capacity(Ah)'))
        #self.charge_capacity_stats = charge_capacity_stats #Arbin: 'Charge_Capacity(Ah)' | Land: 'SpeCapC/mAh/g'
        #self.discharge_capacity_stats = discharge_capacity_stats #Arbin: 'Discharge_Capacity(Ah)' | Land: 'SpeCapD/mAh/g'
        #self.charge_voltage_stats = charge_voltage_stats #Arbin: 'Voltage(V)' | Land: 'MedVoltC/V'
        #self.discharge_voltage_stats = discharge_voltage_stats #Arbin: 'Voltage' | Land: 'MedVoltD/V'
        #self.efficency_stats = efficiency_stats #Land: 'Efficiency/%'
