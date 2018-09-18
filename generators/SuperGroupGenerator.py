import parameters.Constants as Constants
from models.Group import Group
from util.ProcessUtil import calculate_group_in_super_group, calculate_group_period_in_seconds
from models.GroupLinkPeriodPercentage import GroupLinkPeriodPercentage


def generate(end_devices):
    if __is_valid_group_count(calculate_group_in_super_group(), len(end_devices)):
        return []

    groupid_to_end_devices = __create_group_id_to_end_devices_dictionary(end_devices)

    return __create_super_group(groupid_to_end_devices)


def __is_valid_group_count(group_number, end_device_number):
    return group_number >= end_device_number


def __create_group_id_to_end_devices_dictionary(end_devices):
    groupid_to_end_devices = {}

    for end_device in end_devices:
        end_device_id = getattr(end_device, '_id')
        group_id = end_device_id[::-1][:Constants.GROUP_ID_LENGTH_IN_BIT][::-1]
        if groupid_to_end_devices.get(group_id) is None:
            groupid_to_end_devices[group_id] = [end_device]
        else:
            groupid_to_end_devices[group_id].append(end_device)

    return groupid_to_end_devices


def __create_super_group(groupid_to_end_devices):
    super_group = []
    group_period = calculate_group_period_in_seconds()

    for group_id in groupid_to_end_devices:
        group = Group(group_id, groupid_to_end_devices[group_id])
        group.configure_link_periods(
            group_period,
            GroupLinkPeriodPercentage(
                Constants.GROUP_UPLINK_PERIOD_PERCENTAGE,
                Constants.GROUP_MIDLINK_PERIOD_PERCENTAGE,
                Constants.GROUP_DOWNLINK_PERIOD_PERCENTAGE
            )
        )
        group.organize_end_devices_by_sf()

        super_group.append(group)

    return super_group
