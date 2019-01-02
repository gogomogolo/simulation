from tasks.subtasks.GroupTransmissionObserver import GroupTransmissionObserver


def generate(group):
    group_id = getattr(group, '_Group__id')
    sf = getattr(group, "_Group__sf")
    end_devices = getattr(group, '_Group__end_devices')
    time_slot_number = getattr(group, "_Group__time_slot_number")

    return GroupTransmissionObserver(group_id, sf, end_devices, time_slot_number)
