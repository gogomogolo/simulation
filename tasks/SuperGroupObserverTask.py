import threading
import generators.GroupUplinkTransmissionObserverGenerator as GroupUplinkTransmissionObserverGenerator
import generators.GroupTransmissionObserverGenerator as GroupTransmissionObserverGenerator
import util.ProcessUtil as ProcessUtil


class SuperGroupObserverTask(threading.Thread):
    def __init__(self, super_group, barrier):
        self.__id = "Thread-{}".format(getattr(super_group, "_SuperGroup__id"))
        self.__observed_sf = getattr(super_group, "_SuperGroup__sf")
        self.__super_group = super_group
        self.__barrier = barrier
        self.__lifecycle_to_finalized_group_observers = {}
        super(SuperGroupObserverTask, self).__init__(name=self.__id)

    def run(self):
        current_lifecycle = 0
        super_group_period_in_seconds = getattr(self.__super_group, "_SuperGroup__period")
        super_group_lifecycle = ProcessUtil.calculate_super_group_lifecycle(super_group_period_in_seconds)
        try:
            while current_lifecycle < super_group_lifecycle:
                groups = getattr(self.__super_group, "_SuperGroup__groups")
                group_observers = self.__create_group_observers(groups)
                for group_observer in group_observers:
                    group_observer.observe()
                self.__lifecycle_to_finalized_group_observers[current_lifecycle] = group_observers
                current_lifecycle += 1

        finally:
            self.__barrier.wait()

    def __create_group_observers(self, groups):
        return [GroupTransmissionObserverGenerator.generate(group) for group in groups]
