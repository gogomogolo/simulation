from minimizers.QMC import QMC


class AttemptSuperGroup(object):
    def __init__(self, _cycle, _observation_subgroups):
        self.__cycle = _cycle
        self.__group_id_to_aggregated_acknowledgement_with_bexpr = {
            getattr(_observation_subgroup, "_GroupTransmissionObserver__group_id"):
            self.__create_acknowledgements_with_bexpr(
                getattr(_observation_subgroup, "_GroupTransmissionObserver__attempt_to_successful_transmitters"),
                getattr(_observation_subgroup, "_GroupTransmissionObserver__group_id"))
            for _observation_subgroup in _observation_subgroups
        }
        self.__group_id_to_aggregated_acknowledgement_without_bexpr = {
            getattr(_observation_subgroup, "_GroupTransmissionObserver__group_id"):
                self.__create_acknowledgements_without_bexpr(
                    getattr(_observation_subgroup, "_GroupTransmissionObserver__attempt_to_successful_transmitters"),
                    getattr(_observation_subgroup, "_GroupTransmissionObserver__group_id"))
            for _observation_subgroup in _observation_subgroups
        }
        self.__group_id_to_transmission_count = {
            getattr(_observation_subgroup, "_GroupTransmissionObserver__group_id"):
                getattr(_observation_subgroup, "_GroupTransmissionObserver__attempt_to_transmission_count").get(self.__cycle+1)
            for _observation_subgroup in _observation_subgroups
        }
        self.__group_id_to_successful_transmissions_not_cumulative = {
            getattr(_observation_subgroup, "_GroupTransmissionObserver__group_id"):
                len(self.__isNone(getattr(_observation_subgroup, "_GroupTransmissionObserver__attempt_to_successful_transmitters").get(self.__cycle+1)))
            for _observation_subgroup in _observation_subgroups
        }
        self.__group_id_to_successful_transmissions = {
            getattr(_observation_subgroup, "_GroupTransmissionObserver__group_id"):
            len(getattr(_observation_subgroup, "_GroupTransmissionObserver__successful_transmitters"))
            for _observation_subgroup in _observation_subgroups
        }
        self.__group_id_to_failed_transmissions = {
            getattr(_observation_subgroup, "_GroupTransmissionObserver__group_id"):
            len(getattr(_observation_subgroup, "_GroupTransmissionObserver__failed_transmitters"))
            for _observation_subgroup in _observation_subgroups
        }
        self.__group_id_to_idle_transmissions = {
            getattr(_observation_subgroup, "_GroupTransmissionObserver__group_id"):
            len(getattr(_observation_subgroup, "_GroupTransmissionObserver__idle_transmitters"))
            for _observation_subgroup in _observation_subgroups
        }

    def __create_acknowledgements_without_bexpr(self, successful_transmitters, group_id):
        if successful_transmitters.get(self.__cycle+1) is None:
            return [""]
        else:
            succeeded_t = successful_transmitters.get(self.__cycle + 1)
            end_device_ids = []
            for end_device in succeeded_t:
                end_device_ids.append(getattr(end_device, '_id')[:(len(getattr(end_device, '_id')) - len(group_id))])

            return set(end_device_ids)

    def __create_acknowledgements_with_bexpr(self, successful_transmitters, group_id):
        if successful_transmitters.get(self.__cycle+1) is None:
            return [""]
        else:
            succeeded_t = successful_transmitters.get(self.__cycle + 1)
            end_device_ids = []
            for end_device in succeeded_t:
                end_device_ids.append(int(getattr(end_device, '_id')[:(len(getattr(end_device, '_id')) - len(group_id))], base=2))

            if sum(end_device_ids) == 0:
                return set([getattr(end_device, '_id')[:(len(getattr(end_device, '_id')) - len(group_id))] for end_device in succeeded_t])

            qmc = QMC(end_device_ids)
            return qmc.minimize()

    def __isNone(self, list):
        if list is None:
            return []
        return list
