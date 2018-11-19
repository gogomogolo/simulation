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
        self.__group_id_to_successful_transmissions = {
            getattr(_observation_subgroup, "_GroupUplinkTransmissionObserver__group_id"):
            len(getattr(_observation_subgroup, "_GroupUplinkTransmissionObserver__end_devices_success_transmission"))
            for _observation_subgroup in _observation_subgroups
        }
        self.__group_id_to_failed_transmissions = {
            getattr(_observation_subgroup, "_GroupUplinkTransmissionObserver__group_id"):
            len(getattr(_observation_subgroup, "_GroupUplinkTransmissionObserver__end_devices_fail_transmission"))
            for _observation_subgroup in _observation_subgroups
        }
        self.__group_id_to_suspended_transmissions = {
            getattr(_observation_subgroup, "_GroupUplinkTransmissionObserver__group_id"):
            getattr(_observation_subgroup, "_GroupUplinkTransmissionObserver__observable_end_devices_count")
            for _observation_subgroup in _observation_subgroups
        }

    def __create_acknowledgements(self, successful_transmitters, group_id):
        end_device_ids = []
        for end_device in successful_transmitters:
            end_device_ids.append(int(getattr(end_device, '_id')[:(len(getattr(end_device, '_id')) - len(group_id))], base=2))

        qmc = QMC(end_device_ids)
        return qmc.minimize()
