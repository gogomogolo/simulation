import parameters.Constants as Constants
import math


def calculate_group_number_in_super_group(super_group_period_in_seconds, group_period_with_delay_in_seconds):
    return int(super_group_period_in_seconds / group_period_with_delay_in_seconds)


def calculate_group_id_length_in_bits(group_count_in_super_group):
    return int(math.ceil(math.log(group_count_in_super_group, 2)))


def calculate_group_period_in_seconds(sf_message_period_in_seconds):
    return Constants.GROUP_LENGTH_IN_SECONDS + sf_message_period_in_seconds


def calculate_time_slot_in_group_ul(sf_message_period_in_seconds):
    return int(Constants.GROUP_LENGTH_IN_SECONDS / sf_message_period_in_seconds)


def calculate_group_period_with_delay_in_seconds(sf_message_period_in_seconds):
    return sf_message_period_in_seconds * float(100/Constants.DUTY_CYCLE_IN_PERCENTAGE)


def calculate_super_group_lifecycle(super_group_period_in_seconds):
    return int(Constants.SIMULATION_LIFE_TIME_IN_SECONDS / super_group_period_in_seconds)


def calculate_active_transmitters_of_group(sf, end_device_num_of_group):
    return int(Constants.SF_TO_ACTIVATION_PROB[sf]*end_device_num_of_group)

