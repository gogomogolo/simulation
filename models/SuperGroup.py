class SuperGroup(object):
    def __init__(self, sf, groups, period, max_group_number):
        self.__id = "SuperGroup-SF:{}".format(str(sf))
        self.__sf = sf
        self.__groups = groups
        self.__period = period
        self.__max_group_number = max_group_number


