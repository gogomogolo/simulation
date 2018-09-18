import parameters.Constants as Constants

from contracts.Distribution import Distribution
from models.EndDevice import EndDevice
from random import shuffle
from util.ListUtil import spread


def distribute(distribution):
    end_devices = []

    if isinstance(distribution, Distribution):
        probability = distribution.pf()
        normalized = [p/sum(probability) for p in probability]

        end_device_distribution = [int(v*Constants.END_DEVICE_NUMBER) for v in normalized]
        spread(end_device_distribution, Constants.END_DEVICE_NUMBER-sum(end_device_distribution))

        if len(end_device_distribution) == len(Constants.SFs):
            device_id = 0

            for i in range(0, len(Constants.SFs)):
                for j in range(0, end_device_distribution[i]):
                    end_devices.append(EndDevice(bin(device_id+j)[2:], Constants.SFs[i]))
                device_id += end_device_distribution[i]

    shuffle(end_devices)

    change_ids(end_devices)

    return end_devices


def change_ids(end_devices):
    _id = 0
    for end_device in end_devices:
        setattr(end_device, '_id', bin(_id)[2:])
        _id += 1

