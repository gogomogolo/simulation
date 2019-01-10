import util.ProcessUtil as ProcessUtil
import util.LogUtil as LogUtil
import random


class GroupTransmissionObserver(object):
    def __init__(self, group_id, sf, end_devices, time_slot_number):
        self.__group_id = group_id
        self.__sf = sf
        self.__group_device_number = len(end_devices)
        self.__time_slot_number = time_slot_number
        self.__attempt = 0
        self.__idle_transmitters = end_devices.copy()
        self.__successful_transmitters = []
        self.__failed_transmitters = []
        self.__random = random.Random()
        self.__seeds = []

    def observe(self):
        observable_idle_device_amount = len(self.__idle_transmitters)
        failed_transmitters = self.__failed_transmitters
        resource_usages = self.__monitor_resource_usages(observable_idle_device_amount, failed_transmitters)
        self.__update_transmissions_state(resource_usages)
        self.__attempt += 1

        LogUtil.get_file_logger(__name__).info(
            '| <Attempt> : %s | <SF> : %s | <GroupId> : %s | <DeviceAmount> : %s | <TimeSlotAmount> : %s | '
            '<IdleTransmittersAmount> : %s '
            '| <SuccessfulTransmittersAmount> : %s | <FailedTransmittersAmount> : %s |',
            str(self.__attempt), str(self.__sf), str(self.__group_id), str(self.__group_device_number),
            str(self.__time_slot_number), str(len(self.__idle_transmitters)),
            str(len(self.__successful_transmitters)), str(len(self.__failed_transmitters)))

    def __update_transmissions_state(self, resource_usages):
        for resource in resource_usages:
            resource_consumers = resource_usages[resource]
            if self.__is_collision(resource_consumers):
                self.__failed_transmitters += resource_consumers
            else:
                self.__successful_transmitters += resource_consumers
        self.__update_fail_transmissions()

    def __is_collision(self, resource_consumers):
        return len(resource_consumers) > 1

    def __update_fail_transmissions(self):
        succeeded_transmitters = {
            getattr(succeeded_transmitter, "_id"): ' '
            for succeeded_transmitter in self.__successful_transmitters
        }

        index = 0
        for failed_transmitter in self.__failed_transmitters:
            transmitter_id = getattr(failed_transmitter, "_id")
            if succeeded_transmitters.get(transmitter_id) is not None:
                self.__failed_transmitters.pop(index)
            else:
                index += 1

    def __monitor_resource_usages(self, observable_idle_device_amount, failed_transmitters):
        used_resources = self.__find_used_time_slots(observable_idle_device_amount, len(failed_transmitters))
        active_transmitters = self.__find_active_transmitters(observable_idle_device_amount)
        transmitters = active_transmitters + failed_transmitters
        failed_transmitters.clear()
        resource_usage = self.__compose_resource_usages(used_resources, transmitters)
        return resource_usage

    def __find_used_time_slots(self, observable_idle_device_amount, failed_transmitters_num):
        time_slots = []
        active_transmitters_amount = \
            ProcessUtil.calculate_active_transmitters_of_group(self.__sf, observable_idle_device_amount)
        transmitters_amount = active_transmitters_amount + failed_transmitters_num
        for i in range(0, transmitters_amount):
            time_slots.append(random.randint(0, self.__time_slot_number - 1))
        return time_slots

    def __find_active_transmitters(self, observable_idle_device_amount):
        active_transmitters_amount = \
            ProcessUtil.calculate_active_transmitters_of_group(self.__sf, observable_idle_device_amount)
        active_transmitters_indexes = \
            self.__select_active_transmitters_index(active_transmitters_amount, observable_idle_device_amount)
        active_transmitters = []
        for index in active_transmitters_indexes:
            active_transmitters.append(self.__idle_transmitters.pop(index))

        return active_transmitters

    def __select_active_transmitters_index(self, transmitters_amount, observable_idle_device_amount):
        seed = self.__random.randint(1, 30000)
        self.__random.seed(seed)
        indexes = self.__random.sample(range(0, observable_idle_device_amount - 1), transmitters_amount)
        self.__seeds.append(seed)
        indexes.sort(reverse=True)
        return indexes

    def __compose_resource_usages(self, used_resources, transmitters):
        resource_usages = {}
        for index in range(0, len(used_resources)):
            if resource_usages.get(used_resources[index]) is None:
                resource_usages[used_resources[index]] = [transmitters[index]]
            else:
                resource_usages[used_resources[index]].append(transmitters[index])
        return resource_usages
