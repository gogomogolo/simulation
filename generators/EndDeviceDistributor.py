import parameters.Constants as Constants
import math

from contracts.Distribution import Distribution
from models.EndDevice import EndDevice
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
                    end_devices.append(EndDevice(__get_bit_format(device_id+j), Constants.SFs[i]))
                device_id += end_device_distribution[i]

    return end_devices


def __get_bit_format(_id):
    _id_length = math.ceil(math.log(Constants.END_DEVICE_NUMBER, 2))
    _id_bit_notation = '0'+str(_id_length)+'b'
    return format(_id, _id_bit_notation)
