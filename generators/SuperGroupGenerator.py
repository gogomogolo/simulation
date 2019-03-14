import parameters.Constants as Constants
import util.LorawanUtil as LorawanUtil
import util.ProcessUtil as ProcessUtil
import util.LogUtil as LogUtil

from models.Group import Group
from models.SuperGroup import SuperGroup

import random


def generate(end_devices):
    sf_to_end_devices = __create_sf_to_end_devices(end_devices)

    return __create_super_groups_with_max_duty_cycle_wait_time(sf_to_end_devices)


def __create_super_groups_with_max_duty_cycle_wait_time(sf_to_end_devices):
    super_groups = []
    sf_to_toa = {}

    for sf in sf_to_end_devices:
        time_on_air = __get_time_on_air(sf)
        sf_to_toa[sf] = time_on_air

    max_toa = sf_to_toa[max(sf_to_toa, key=lambda x: sf_to_toa.get(x))]

    for sf in sf_to_end_devices:
        time_on_air = __get_time_on_air(sf)
        group_period_in_seconds = ProcessUtil.calculate_group_period_in_seconds(time_on_air)
        group_period_with_delay_in_seconds = ProcessUtil.calculate_group_period_with_delay_in_seconds(max_toa)
        __fill_and_log(super_groups, time_on_air, sf, sf_to_end_devices, group_period_in_seconds, group_period_with_delay_in_seconds)

    return super_groups


def __create_super_groups(sf_to_end_devices):
    super_groups = []

    for sf in sf_to_end_devices:
        time_on_air = __get_time_on_air(sf)
        group_period_in_seconds = ProcessUtil.calculate_group_period_in_seconds(time_on_air)
        group_period_with_delay_in_seconds = ProcessUtil.calculate_group_period_with_delay_in_seconds(time_on_air)
        __fill_and_log(super_groups, time_on_air, sf, sf_to_end_devices, group_period_in_seconds, group_period_with_delay_in_seconds)

    return super_groups


def __fill_and_log(super_groups, toa, sf, sf_to_end_devices, group_period_in_seconds, group_period_with_delay_in_seconds):
    super_group_period_in_seconds = Constants.SF_TO_SUPER_GROUP_PERIOD_IN_SEC.get(sf)
    attempt_count = int(Constants.SIMULATION_LIFE_TIME_IN_SECONDS / super_group_period_in_seconds)

    group_number_in_super_group = \
        ProcessUtil.calculate_group_number_in_super_group(super_group_period_in_seconds,
                                                          group_period_with_delay_in_seconds)
    group_id_length_in_bits = ProcessUtil.calculate_group_id_length_in_bits(group_number_in_super_group)
    exact_group_number = (2 ** group_id_length_in_bits)
    time_slot_in_upper_link = ProcessUtil.calculate_time_slot_in_group_ul(toa)

    group_id_to_end_devices = __create_group_id_to_end_devices(sf_to_end_devices[sf], group_id_length_in_bits)
    __distribute_transmission_attempt(group_id_to_end_devices, attempt_count)
    super_group = __create_super_group(group_id_to_end_devices, sf, toa,
                                       time_slot_in_upper_link, group_period_in_seconds)

    super_groups.append(SuperGroup(sf, super_group, super_group_period_in_seconds, exact_group_number))

    LogUtil.get_file_logger(__name__).info(
        '| <SF> : %s | <DeviceAmount> : %s | <SuperGroupPeriodSec> : %s | '
        '<GroupPeriodSec> : %s '
        '| <GroupPeriodWithDelaySec> : %s | <GroupNumber> : %s |',
        str(sf), str(len(sf_to_end_devices[sf])), str(super_group_period_in_seconds),
        str(group_period_in_seconds), str(group_period_with_delay_in_seconds), str(exact_group_number))


def __distribute_transmission_attempt(group_id_to_end_devices, attempt_count):

    for gid in group_id_to_end_devices:
        _random = random.Random()
        seed = _random.randint(1, 30000)
        _random.seed(seed)

        devices = group_id_to_end_devices.get(gid)
        uniform_transmission_attempt = {attempt: int(len(devices)/attempt_count) for attempt in range(1, attempt_count+1)}
        excluded_attempt = []
        for device in devices:
            if len(excluded_attempt) != attempt_count:
                attempt = _random.sample([x for x in range(1, attempt_count + 1) if x not in excluded_attempt], 1)[0]
                uniform_transmission_attempt[attempt] = uniform_transmission_attempt.get(attempt)-1
                device.set_transmitting_attempt(attempt)
                if uniform_transmission_attempt[attempt] == 0:
                    excluded_attempt.append(attempt)
            else:
                attempt = _random.randint(1, attempt_count)
                device.set_transmitting_attempt(attempt)


def __create_sf_to_end_devices(end_devices):
    sf_to_end_devices = {}

    for end_device in end_devices:
        sf = getattr(end_device, "_sf")
        if sf_to_end_devices.get(sf) is None:
            sf_to_end_devices[sf] = [end_device]
        else:
            sf_to_end_devices[sf].append(end_device)

    return sf_to_end_devices


def __create_group_id_to_end_devices(end_devices, group_id_length_in_bits):
    groupid_to_end_devices = {}

    for end_device in end_devices:
        end_device_id = getattr(end_device, '_id')
        group_id = end_device_id[::-1][:group_id_length_in_bits][::-1]
        if groupid_to_end_devices.get(group_id) is None:
            groupid_to_end_devices[group_id] = [end_device]
        else:
            groupid_to_end_devices[group_id].append(end_device)

    return groupid_to_end_devices


def __create_super_group(group_id_to_end_devices, sf, time_on_air, time_slot_in_upper_link, group_period_in_seconds):
    super_group = []

    for group_id in group_id_to_end_devices:
        group = Group(group_id, sf, group_id_to_end_devices[group_id],
                      time_on_air, time_slot_in_upper_link, group_period_in_seconds)
        super_group.append(group)

    return super_group


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
