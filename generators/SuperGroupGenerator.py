import parameters.Constants as Constants
import util.LorawanUtil as LorawanUtil
import util.ProcessUtil as ProcessUtil
import util.LogUtil as LogUtil

from models.Group import Group
from models.SuperGroup import SuperGroup


def generate(end_devices):
    sf_to_end_devices = __create_sf_to_end_devices(end_devices)

    return __create_super_groups(sf_to_end_devices)


def __create_super_groups(sf_to_end_devices):
    super_groups = []

    for sf in sf_to_end_devices:
        time_on_air = __get_time_on_air(sf)
        group_period_in_seconds = ProcessUtil.calculate_group_period_in_seconds(time_on_air)
        group_period_with_delay_in_seconds = ProcessUtil.calculate_group_period_with_delay_in_seconds(time_on_air)
        super_group_period_in_seconds = Constants.SF_TO_SUPER_GROUP_PERIOD_IN_SEC.get(sf)

        group_number_in_super_group = \
            ProcessUtil.calculate_group_number_in_super_group(super_group_period_in_seconds,
                                                              group_period_with_delay_in_seconds)
        group_id_length_in_bits = ProcessUtil.calculate_group_id_length_in_bits(group_number_in_super_group)
        time_slot_in_upper_link = ProcessUtil.calculate_time_slot_in_group_ul(time_on_air)

        group_id_to_end_devices = __create_group_id_to_end_devices(sf_to_end_devices[sf], group_id_length_in_bits)
        super_group = __create_super_group(group_id_to_end_devices, sf, time_on_air,
                                           time_slot_in_upper_link, group_period_in_seconds)

        super_groups.append(SuperGroup(sf, super_group, super_group_period_in_seconds, group_number_in_super_group))

        LogUtil.get_file_logger(__name__).info(
            '| <SF> : %s | <DeviceAmount> : %s | <SuperGroupPeriodSec> : %s | '
            '<GroupPeriodSec> : %s '
            '| <GroupPeriodWithDelaySec> : %s | <GroupNumber> : %s |',
            str(sf), str(len(sf_to_end_devices[sf])), str(super_group_period_in_seconds),
            str(group_period_in_seconds), str(group_period_with_delay_in_seconds), str(group_number_in_super_group))

    return super_groups


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
