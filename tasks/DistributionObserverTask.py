import threading
import parameters.Constants as Constants
import time
from random import randrange

from util.LorawanUtil import calculate_time_on_air
from util.ProcessUtil import calculate_time_slot_in_group_ul
from distributions.Bernoulli import Bernoulli


class DistributionObserverTask(threading.Thread):
    def __init__(self, group_id, sf, end_devices, uplink_period_in_second):
        self.__group_id = group_id
        self.__sf = sf
        self.__end_devices = end_devices.copy()
        self.__end_devices_success_transmission = []
        self.__end_devices_fail_transmission = []
        self.__message_period_in_seconds = calculate_time_on_air(
            Constants.BANDWIDTH_IN_HERTZ,
            Constants.NUMBER_OF_PREAMBLE,
            Constants.SYNCHRONIZATION_WORD,
            Constants.SF_TO_MAC_PAYLOAD_IN_BYTE[sf],
            sf,
            Constants.CRC,
            Constants.IH,
            Constants.DE,
            Constants.CODING_RATE)
        self.__time_slot_number = calculate_time_slot_in_group_ul(
            uplink_period_in_second,
            self.__message_period_in_seconds)
        self.__observable_end_devices_count = len(end_devices)
        super(DistributionObserverTask, self).__init__(name="Thread-GroupID-{}".format(str(group_id)))

    def run(self):
        cycle = 0
        distribution = self.__create_distribution()

        while cycle < self.__time_slot_number:
            self.__observe_transmission_of_end_devices(distribution)
            cycle += 1
            self.__change_distribution(distribution)
            time.sleep(self.__message_period_in_seconds)

    def __create_distribution(self):
        return Bernoulli(self.__observable_end_devices_count,
                         float(randrange(1, 10)) / float(self.__observable_end_devices_count))

    def __change_distribution(self, distribution):
        setattr(distribution, 'size', self.__observable_end_devices_count)
        setattr(distribution, 'p', float(randrange(1, 10)) / float(self.__observable_end_devices_count))

    def __observe_transmission_of_end_devices(self, distribution):
        transmissions = distribution.sample()
        if self.__are_valid_transmissions(transmissions):
            self.__update_end_device_container(transmissions, self.__end_devices_success_transmission)
        else:
            self.__update_end_device_container(transmissions, self.__end_devices_fail_transmission)

    def __are_valid_transmissions(self, transmissions):
        return sum(transmissions) <= 1

    def __is_there_transmitter(self, transmissions):
        return transmissions.count(1) != 0

    def __update_end_device_container(self, transmissions, expected_updatable_device_container):
        while self.__is_there_transmitter(transmissions):
            end_device = self.__end_devices.pop(transmissions.index(1))
            expected_updatable_device_container.append(end_device)
            self.__observable_end_devices_count -= 1
            transmissions.remove(1)

