from util.ProcessUtil import calculate_link_period_in_seconds


class Group(object):
    def __init__(self, _id, _end_devices):
        self.__id = _id
        self.__end_devices = _end_devices
        self.__uplink_period_in_seconds = 0
        self.__downlink_period_in_seconds = 0
        self.__midlink_period_in_seconds = 0
        self.__sf_to_end_devices = {}

    def configure_link_periods(self, period_in_seconds, link_period_percentage):
        self.__configure_uplink_period(
            calculate_link_period_in_seconds(period_in_seconds,
                                             getattr(link_period_percentage, '__uplink_period_percentage'))
        )
        self.__configure_midlink_period(
            calculate_link_period_in_seconds(period_in_seconds,
                                             getattr(link_period_percentage, '__midlink_period_percentage'))
        )
        self.__configure_downlink_period(
            calculate_link_period_in_seconds(period_in_seconds,
                                             getattr(link_period_percentage, '__downlink_period_percentage'))
        )

    def organize_end_devices_by_sf(self):
        for end_device in self.__end_devices:
            end_device_sf = getattr(end_device, '_sf')
            if self.__sf_to_end_devices.get(end_device_sf) is None:
                self.__sf_to_end_devices[end_device_sf] = [end_device]
            else:
                self.__sf_to_end_devices[end_device_sf].append(end_device)

    def __configure_uplink_period(self, period_in_seconds):
        self.__uplink_period_in_seconds = period_in_seconds

    def __configure_midlink_period(self, period_in_seconds):
        self.__midlink_period_in_seconds = period_in_seconds

    def __configure_downlink_period(self, period_in_seconds):
        self.__downlink_period_in_seconds = period_in_seconds
