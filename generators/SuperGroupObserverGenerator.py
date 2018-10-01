from tasks.SuperGroupObserverTask import SuperGroupObserverTask


def generate(super_group, barrier):
    return SuperGroupObserverTask(super_group, barrier)
