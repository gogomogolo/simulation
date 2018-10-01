from minimizers.QMC import QMC


class LifecycleGroup(object):
    def __init__(self, _cycle, _observation_subgroups):
        self.__cycle = _cycle
        self.__group_id_to_aggregated_acknowledgement = {
            getattr(_observation_subgroup, "_GroupUplinkTransmissionObserver__group_id"):
            self.__create_acknowledgements(
                getattr(_observation_subgroup, "_GroupUplinkTransmissionObserver__end_devices_success_transmission"),
                getattr(_observation_subgroup, "_GroupUplinkTransmissionObserver__group_id"))
            for _observation_subgroup in _observation_subgroups
        }

    def __create_acknowledgements(self, successful_transmitters, group_id):
        end_device_ids = \
            [int(getattr(end_device, '_id')[:(len(getattr(end_device, '_id')) - len(group_id))], base=2)
             for end_device in successful_transmitters]
        return QMC(end_device_ids)
