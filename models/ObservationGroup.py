import generators.LifecycleGroupGenerator as LifecycleGroupGenerator
import generators.AttemptSuperGroupGenerator as AttemptSuperGroupGenerator


class ObservationGroup(object):
    def __init__(self, _sf, _lifecycle_to_finalized_observation_group):
        self.__sf = _sf
        self.__lifecycles = \
            [AttemptSuperGroupGenerator.generate(_lifecycle, _lifecycle_to_finalized_observation_group[_lifecycle])
             for _lifecycle in _lifecycle_to_finalized_observation_group]
