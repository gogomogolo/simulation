from tasks.UplinkTransmissionObserverTask import UplinkTransmissionObserverTask


def generate(group, barrier):
    observer_tasks = []
    group_id = getattr(group, '_Group__id')
    sf_to_end_devices = getattr(group, '_Group__sf_to_end_devices')
    uplink_period_in_seconds = getattr(group, '_Group__uplink_period_in_seconds')

    for sf in sf_to_end_devices:
        observer_tasks.append(
            UplinkTransmissionObserverTask(group_id, sf, sf_to_end_devices[sf], uplink_period_in_seconds, barrier)
        )

    return observer_tasks
