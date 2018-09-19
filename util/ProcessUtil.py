import parameters.Constants as Constants


def calculate_group_in_super_group():
    return 2**Constants.GROUP_ID_LENGTH_IN_BIT


def calculate_group_period_in_seconds():
    return Constants.SUPER_GROUP_LENGTH_IN_SECONDS / float(calculate_group_in_super_group())


def calculate_link_period_in_seconds(group_period_in_seconds, space_percentage):
    return group_period_in_seconds*space_percentage


def calculate_time_slot_in_group_ul(group_ul_period_in_seconds, sf_message_period_in_seconds):
    return int(group_ul_period_in_seconds / sf_message_period_in_seconds)
