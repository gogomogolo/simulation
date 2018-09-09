import parameters.Constants as Constants

from minimizers.QuineMcCluskey import QuineMcCluskey
from distributions.Exponential import Exponential
from distributions.Bernoulli import Bernoulli
from models.EndDevice import EndDevice
from models.Gateway import Gateway
from generators.EndDeviceDistributor import distribute
from time import sleep

message_transferable_eds = []
message_transferred_eds = []
message_untransferable_eds = []


def run():
    global message_transferable_eds
    global message_transferred_eds
    global message_untransferable_eds

    end_device_message_period = Constants.END_DEVICE_MESSAGE_PERIOD
    gateway_message_period = Constants.GATEWAY_MESSAGE_PERIOD
    spreading_factors = Constants.SFs
    bernoulli_size = Constants.BERNOULLI_DIST_SIZE
    bernoulli_p = Constants.BERNOULLI_DIST_P
    exponential_size = Constants.EXPONENTIAL_DIST_SIZE
    exponential_scale = Constants.EXPONENTIAL_DIST_SCALE

    bernoulli = Bernoulli(bernoulli_size, bernoulli_p)
    exponential = Exponential(exponential_size, exponential_scale)

    end_devices = distribute(exponential)
    gateway = Gateway("GW1", end_devices)

    message_transferable_eds = [x for x in range(0, len(end_devices))]

    occurrence = 0

    while (gateway_message_period / end_device_message_period) != occurrence:
        index_of_transmiters = send_message(bernoulli)
        update_transmission_status(end_devices, index_of_transmiters)
        occurrence += 1
        sleep(end_device_message_period)


def send_message(distribution):
    global message_transferable_eds
    observation = distribution.sample()
    return [x for x in range(0, len(observation)) if observation[x] == 1 and x in message_transferable_eds]


def update_transmission_status(end_devices, index_of_transmiters):
    global message_untransferable_eds
    global message_transferred_eds
    global message_transferable_eds

    sf_to_index = {}

    for index in index_of_transmiters:
        ed = end_devices[index]
        sf_of_ed = getattr(ed, "_sf")

        if sf_to_index.get(sf_of_ed) is None:
            sf_to_index[sf_of_ed] = [index]
        else:
            sf_to_index[sf_of_ed].append(index)

    for sf in sf_to_index:
        if len(sf_to_index.get(sf)) > 1:
            message_untransferable_eds += sf_to_index.get(sf)
        else:
            message_transferred_eds += sf_to_index.get(sf)

    message_transferable_eds = [x for x in range(0, len(end_devices)) if x not in message_untransferable_eds and x not in message_transferred_eds]