from distributions.Bernoulli import Bernoulli


class GroupUplinkTransmissionObserver(object):
    def __init__(self, group_id, sf, end_devices, time_slot_number):
        self.__group_id = group_id
        self.__sf = sf
        self.__end_devices = end_devices.copy()
        self.__end_devices_success_transmission = []
        self.__end_devices_fail_transmission = []
        self.__observable_end_devices_count = len(end_devices)
        self.__time_slot_number = time_slot_number

    def observe(self):
        cycle = 0
        while self.__is_valid_observation(cycle):
            self.__observe_transmission_of_end_devices()
            cycle += 1

    def __observe_transmission_of_end_devices(self):
        distribution = Bernoulli(self.__observable_end_devices_count, (float(1) / float(self.__observable_end_devices_count)))
        transmissions = list(distribution.sample())
        if self.__are_valid_transmissions(transmissions):
            self.__update_end_device_container(transmissions, self.__end_devices_success_transmission)
        else:
            self.__update_end_device_container(transmissions, self.__end_devices_fail_transmission)

    def __is_valid_observation(self, cycle):
        return cycle < self.__time_slot_number and self.__observable_end_devices_count > 0

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

