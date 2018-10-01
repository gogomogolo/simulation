class Group(object):
    def __init__(self, _id, _sf, _end_devices, _time_on_air_in_seconds, _time_slot_in_upper_link, _group_period_in_seconds):
        self.__id = _id
        self.__end_devices = _end_devices
        self.__sf = _sf
        self.__message_period_of_one_time_slot_in_seconds = _time_on_air_in_seconds
        self.__time_slot_number = _time_slot_in_upper_link
        self.__period = _group_period_in_seconds
