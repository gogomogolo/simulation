class GroupLinkPeriodPercentage(object):
    def __init__(self, _uplink_period_percentage, _midlink_period_percentage, _downlink_period_percentage):
        if (_uplink_period_percentage + _midlink_period_percentage + _downlink_period_percentage) == 1:
            self.__uplink_period_percentage = _uplink_period_percentage
            self.__midlink_period_percentage = _midlink_period_percentage
            self.__downlink_period_percentage = _downlink_period_percentage
