import util.LogUtil as LogUtil
import random


class GroupTransmissionObserver(object):
    def __init__(self, group_id, sf, end_devices, time_slot_number):
        self.__group_id = group_id
        self.__sf = sf
        self.__group_device_number = len(end_devices)
        self.__end_devices = end_devices.copy()
        self.__time_slot_number = time_slot_number
        self.__attempt = 1
        self.__idle_transmitters = []
        self.__successful_transmitters = []
        self.__attempt_to_successful_transmitters = {}
        self.__attempt_to_transmission_count = {}
        self.__failed_transmitters = []
        self.__random = random.Random()
        self.__seeds = []

    def observe(self):
        resource_usages = self.__monitor_resource_usages()
        self.__update_transmissions_state(resource_usages)

        self.__idle_transmitters = [device for device in self.__end_devices if device.transmission_status == "NONE"]
        self.__successful_transmitters = [device for device in self.__end_devices if device.transmission_status == "SUCCEEDED"]
        self.__failed_transmitters = [device for device in self.__end_devices if device.transmission_status == "FAILED"]

        LogUtil.get_file_logger(__name__).info(
            '| <Attempt> : %s | <SF> : %s | <GroupId> : %s | <DeviceAmount> : %s | <TimeSlotAmount> : %s | '
            '<IdleTransmittersAmount> : %s '
            '| <SuccessfulTransmittersAmount> : %s | <FailedTransmittersAmount> : %s |',
            str(self.__attempt), str(self.__sf), str(self.__group_id), str(self.__group_device_number),
            str(self.__time_slot_number),
            str(len(self.__idle_transmitters)),
            str(len(self.__successful_transmitters)),
            str(len(self.__failed_transmitters)))

        self.__attempt += 1

    def __update_transmissions_state(self, resource_usages):
        transmission_count = 0
        for resource in resource_usages:
            resource_consumers = resource_usages[resource]
            if self.__is_collision(resource_consumers):
                self.__update_devices_status(resource_consumers, "FAILED")
                self.__retransmission_devices(resource_consumers)
            else:
                self.__update_devices_status(resource_consumers, "SUCCEEDED")
                if self.__attempt_to_successful_transmitters.get(self.__attempt) is None:
                    self.__attempt_to_successful_transmitters[self.__attempt] = [resource_consumers[0]]
                else:
                    self.__attempt_to_successful_transmitters[self.__attempt].append(resource_consumers[0])
            transmission_count += len(resource_consumers)
        self.__attempt_to_transmission_count[self.__attempt] = transmission_count

    def __is_collision(self, resource_consumers):
        return len(resource_consumers) > 1

    def __update_devices_status(self, devices, status):
        for device in devices:
            device.set_transmission_status(status)

    def __retransmission_devices(self, devices):
        for device in devices:
            device.set_transmitting_attempt(self.__attempt+1)
            device.increment_retransmission_attempt_count()

    def __monitor_resource_usages(self):
        active_transmitters = self.__find_active_transmitters()
        used_resources = self.__find_used_time_slots(len(active_transmitters))
        resource_usage = self.__compose_resource_usages(used_resources, active_transmitters)
        return resource_usage

    def __find_used_time_slots(self, active_transmitters_amount):
        time_slots = []
        for i in range(0, active_transmitters_amount):
            time_slots.append(random.randint(0, self.__time_slot_number - 1))
        return time_slots

    def __find_active_transmitters(self):
        active_transmitters = []
        for device in self.__end_devices:
            if device.transmitting_attempt == self.__attempt and device.transmission_status != "SUCCEEDED":
                if device.retransmission_attempt_count != 8:
                    active_transmitters.append(device)

        return active_transmitters

    def __compose_resource_usages(self, used_resources, active_transmitters):
        resource_usages = {}
        for index in range(0, len(used_resources)):
            if resource_usages.get(used_resources[index]) is None:
                resource_usages[used_resources[index]] = [active_transmitters[index]]
            else:
                resource_usages[used_resources[index]].append(active_transmitters[index])
        return resource_usages
