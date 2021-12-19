
class batteryDataSet:
    'Class to provide consistent format for dataset representations'

    def __init__(self,discharge_capacity_stats,charge_voltage_stats=None,discharge_voltage_stats=None,efficiency_stats=None,cyclenumbers=None,speCapData=None,voltageData=None,charge_capacity_stats=None):
        self.cyclenumbers = cyclenumbers
        self.speCapData = speCapData
        self.voltageData = voltageData
        self.charge_capacity_stats = charge_capacity_stats
        self.discharge_capacity_stats = discharge_capacity_stats
        self.charge_voltage_stats = charge_voltage_stats
        self.discharge_voltage_stats = discharge_voltage_stats
        self.efficency_stats = efficiency_stats
        
