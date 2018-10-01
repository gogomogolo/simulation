from models.ObservationGroup import ObservationGroup


def generate(_observation_group):
    sf = getattr(_observation_group, "_SuperGroupObserverTask__observed_sf")
    lifecycle_to_finalized_observation_subgroups = \
        getattr(_observation_group, "_SuperGroupObserverTask__lifecycle_to_finalized_group_observers")
    return ObservationGroup(sf, lifecycle_to_finalized_observation_subgroups)
