def generate(end_devices):
    return __create_sf_to_end_devices(end_devices)


def __create_sf_to_end_devices(end_devices):
    sf_to_end_devices = {}

    for end_device in end_devices:
        sf = getattr(end_device, "_sf")
        if sf_to_end_devices.get(sf) is None:
            sf_to_end_devices[sf] = [end_device]
        else:
            sf_to_end_devices[sf].append(end_device)

    return sf_to_end_devices