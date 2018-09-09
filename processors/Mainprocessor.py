import parameters.Constants as Constants
import parameters.Results as Results

from minimizers.QMC import QMC
from distributions.Exponential import Exponential
from distributions.Bernoulli import Bernoulli
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

    ack_all_devices_with_same_ack(message_transferred_eds)
    ack_all_devices_with_different_ack_respect_to_sf(end_devices, message_transferred_eds)


def send_message(distribution):
    global message_transferable_eds
    observation = distribution.sample()
    return [x for x in range(0, len(observation)) if observation[x] == 1 and x in message_transferable_eds]


def update_transmission_status(end_devices, transmitters_index):
    global message_untransferable_eds
    global message_transferred_eds
    global message_transferable_eds

    sf_to_index = create_sf_to_index_dict(end_devices, transmitters_index)

    for sf in sf_to_index:
        if len(sf_to_index.get(sf)) > 1:
            message_untransferable_eds += sf_to_index.get(sf)
        else:
            message_transferred_eds += sf_to_index.get(sf)

    message_transferable_eds = [x for x in range(0, len(end_devices)) if x not in message_untransferable_eds and x not in message_transferred_eds]


def ack_all_devices_with_same_ack(transmitters_index):
    qmc = QMC(transmitters_index)
    minimized_exp = qmc.minimize()

    for minterm in minimized_exp:
        Results.BOOLEAN_EXP_FOR_SAME_ACK += minterm
        Results.DEVICE_ID_LENGTH_IN_BIT_SAME_ACK = len(minterm)
        Results.MAC_PAYLOAD_IN_BIT_SAME_ACK += len(minterm)*2


def ack_all_devices_with_different_ack_respect_to_sf(end_devices, transmitters_index):
    sf_to_index = create_sf_to_index_dict(end_devices, transmitters_index)

    sf_to_exp = {}

    for sf in sf_to_index:
        qmc = QMC(sf_to_index[sf])
        sf_to_exp[sf] = qmc.minimize()

    for sf in sf_to_exp:
        for minterm in sf_to_exp[sf]:
            if Results.BOOLEAN_EXP_FOR_DIFFERENT_ACK.get(sf) is None:
                Results.BOOLEAN_EXP_FOR_DIFFERENT_ACK[sf] = minterm
                Results.DEVICE_ID_LENGTH_IN_BIT_DIFFERENT_ACK[sf] = len(minterm)
                Results.MAC_PAYLOAD_IN_BIT_DIFFERENT_ACK[sf] = len(minterm)*2
            else:
                Results.BOOLEAN_EXP_FOR_DIFFERENT_ACK[sf] += minterm
                Results.MAC_PAYLOAD_IN_BIT_DIFFERENT_ACK[sf] += len(minterm)*2


def create_sf_to_index_dict(end_devices, transmitters_index):
    sf_to_index = {}

    for index in transmitters_index:
        ed = end_devices[index]
        sf_of_ed = getattr(ed, "_sf")

        if sf_to_index.get(sf_of_ed) is None:
            sf_to_index[sf_of_ed] = [index]
        else:
            sf_to_index[sf_of_ed].append(index)

    return sf_to_index
