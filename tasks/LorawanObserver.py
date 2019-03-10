import parameters.Constants as Constants
import util.LorawanUtil as LorawanUtil
import util.ProcessUtil as ProcessUtil
import random
from models.CommunicationState import CommunicationState


observation_time = Constants.SIMULATION_LIFE_TIME_IN_SECONDS


def start(lorawan_groups):
    communication_history = []

    for sf in lorawan_groups:
        toa = __get_time_on_air(sf)
        devices_of_sf = lorawan_groups.get(sf)
        sf_time_slots_usage = __monitor_resource_usages(sf, toa, devices_of_sf)
        communication_history += [CommunicationState(sf, toa, time_slot, sf_time_slots_usage.get(time_slot))
                                  for time_slot in sf_time_slots_usage]

    communication_history.sort(key=lambda communication_status: communication_status.transmission_time, reverse=False)

    acknowledged_communications = __find_acknowledged_transmissions(communication_history)
    unacknowledged_communications = __find_unacknowledged_retransmissions(communication_history)
    collided_communications = __find_collided_retransmissions(communication_history)
    __find_idle_transmissions(communication_history)


def __monitor_resource_usages(sf, toa, lorawan_sf_devices):
    used_resources = __find_used_time_slots(sf, toa, lorawan_sf_devices)
    active_transmitters = __find_active_transmitters(sf, lorawan_sf_devices)
    resource_usage = __compose_resource_usages(used_resources, active_transmitters)
    return resource_usage


def __find_used_time_slots(sf, toa, lorawan_sf_devices):
    time_slots = []
    lorawan_sf_devices_count = len(lorawan_sf_devices)
    time_slot_number = int(Constants.SIMULATION_LIFE_TIME_IN_SECONDS/toa)
    active_transmitters_count = lorawan_sf_devices_count
    for i in range(0, active_transmitters_count):
        time_slots.append(random.randint(0, time_slot_number - 1))
    return time_slots


def __find_active_transmitters(sf, lorawan_sf_devices):
    lorawan_sf_devices_count = len(lorawan_sf_devices)
    active_transmitters_amount = lorawan_sf_devices_count
    active_transmitters_indexes = \
        __select_active_transmitters_index(active_transmitters_amount, lorawan_sf_devices_count)
    active_transmitters = []
    for index in active_transmitters_indexes:
        active_transmitters.append(lorawan_sf_devices.pop(index))

    return active_transmitters


def __select_active_transmitters_index(active_transmitters_amount, lorawan_sf_devices_count):
    _random = random.Random()
    seed = _random.randint(1, 30000)
    _random.seed(seed)
    indexes = _random.sample(range(0, lorawan_sf_devices_count), active_transmitters_amount)
    indexes.sort(reverse=True)
    return indexes


def __compose_resource_usages(used_resources, active_transmitters):
    resource_usages = {}
    for index in range(0, len(used_resources)):
        if resource_usages.get(used_resources[index]) is None:
            resource_usages[used_resources[index]] = [active_transmitters[index]]
        else:
            resource_usages[used_resources[index]].append(active_transmitters[index])
    return resource_usages


def __find_acknowledged_transmissions(communication_history):
    valid_after_transmission_time = 0
    acknowledged_communications = []
    for communication_status in communication_history:
        if communication_status.is_collision is False and\
                communication_status.second_receive_window_time >= valid_after_transmission_time:
            valid_after_transmission_time = communication_status.second_receive_window_time + \
                                             (communication_status.receiving_message_toa * float(100/Constants.DUTY_CYCLE_IN_PERCENTAGE))
            acknowledged_communications.append(communication_status)

    return acknowledged_communications


def __find_unacknowledged_retransmissions(communication_history):
    valid_after_transmission_time = 0
    valid_transmission_time = 0
    unacknowledged_communications = []

    for communication_status in communication_history:
        if communication_status.is_collision is True:
            continue

        if communication_status.second_receive_window_time >= valid_after_transmission_time:
            valid_transmission_time = communication_status.second_receive_window_time
            valid_after_transmission_time = communication_status.second_receive_window_time + \
                                             (communication_status.receiving_message_toa * float(100/Constants.DUTY_CYCLE_IN_PERCENTAGE))

        elif communication_status.second_receive_window_time > valid_transmission_time and \
                communication_status.second_receive_window_time < valid_after_transmission_time:
            unacknowledged_communications.append(communication_status)

    return unacknowledged_communications


def __find_collided_retransmissions(communication_history):
    collided_communications = []

    for communication_status in communication_history:
        if communication_status.is_collision is True:
            collided_communications.append(communication_status)

    return collided_communications


def __find_idle_transmissions(communication_history):
    for communication_status in communication_history:
        a = 1


def __find_time_slot(time_offset, time_period, time_on_air):
    return float(time_offset+time_period)/time_on_air


def __get_time_on_air(sf):
    return LorawanUtil.calculate_time_on_air(
            Constants.BANDWIDTH_IN_HERTZ,
            Constants.NUMBER_OF_PREAMBLE,
            Constants.SYNCHRONIZATION_WORD,
            Constants.SF_TO_MAC_PAYLOAD_IN_BYTE[sf],
            sf,
            Constants.CRC,
            Constants.IH,
            Constants.DE,
            Constants.CODING_RATE)