import generators.ObservationGroupGenerator as ObservationGroupGenerator


class SimulationResult(object):
    def __init__(self, _finalized_observation_groups):
        self.__observation_groups = [ObservationGroupGenerator.generate(observation_group)
                                     for observation_group in _finalized_observation_groups]
