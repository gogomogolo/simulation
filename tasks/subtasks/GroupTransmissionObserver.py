import util.ProcessUtil as ProcessUtil
import random

class GroupTransmissionObserver(object):
    def __init__(self, group_id, sf, end_devices, time_slot_number):
        self.__group_id = group_id
        self.__sf = sf
        self.__group_device_number = len(end_devices)
        self.__end_devices = end_devices.copy()
        self.__time_slot_number = time_slot_number

    def observe(self):
        transmitters = self.__find_active_transmitters()
        

    def __find_active_transmitters(self):
        transmitters_amount = ProcessUtil.calculate_active_transmitters_of_group(self.__group_device_number)


    def