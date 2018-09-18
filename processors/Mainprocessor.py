import parameters.Constants as Constants
import parameters.Results as Results
import logging
import sys
import generators.UplinkTransmissionObserverGenerator as UplinkTransmissionObserverGenerator
import generators.SuperGroupGenerator as SuperGroupGenerator
import threading

from minimizers.QMC import QMC
from distributions.Exponential import Exponential
from generators.EndDeviceDistributor import distribute

message_transferable_eds = {}
message_transferred_eds = {}
message_untransferable_eds = {}

formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')
screen_handler = logging.StreamHandler(stream=sys.stdout)
screen_handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(screen_handler)
logger.setLevel(logging.DEBUG)


def run():
    logger.info("<run> Simulation is starting...")
    group_id_to_finalized_observers = {}

    exponential_size = Constants.EXPONENTIAL_DIST_SIZE
    exponential_scale = Constants.EXPONENTIAL_DIST_SCALE
    exponential = Exponential(exponential_size, exponential_scale)

    end_devices = distribute(exponential)
    super_group = SuperGroupGenerator.generate(end_devices)

    for group in super_group:
        total_thread_count = __calculate_total_thread_count(group)
        barrier = threading.Barrier(total_thread_count)

        transmission_observers = UplinkTransmissionObserverGenerator.generate(group, barrier)

        for transmission_observer in transmission_observers:
            transmission_observer.start()

        barrier.wait()

        group_id_to_finalized_observers[getattr(group, '__id')] = transmission_observers


    __ack_all_devices_with_same_ack(message_transferred_eds)
    __ack_all_devices_with_different_ack_respect_to_sf(end_devices, message_transferred_eds)

    Results.NUMBER_OF_FAILED_DEVICES = len(message_untransferable_eds)
    Results.NUMBER_OF_TRANSMITTERS = len(message_transferred_eds)
    Results.NUMBER_OF_SUSPENDED_DEVICES = len(message_transferable_eds)


def __calculate_total_thread_count(group):
    sf_to_end_devices = getattr(group, '__sf_to_end_devices')
    return len(sf_to_end_devices) + 1

def __ack_all_devices_with_same_ack(transmitters_index):
    logger.info("<ack_all_devices_with_same_ack> Boolean expressions are being created for acking each devices...")
    qmc = QMC([key for key in transmitters_index])
    minimized_exp = qmc.minimize()

    for minterm in minimized_exp:
        Results.BOOLEAN_EXP_FOR_SAME_ACK += minterm
        Results.DEVICE_ID_LENGTH_IN_BIT_SAME_ACK = len(minterm)
        Results.MAC_PAYLOAD_IN_BIT_SAME_ACK += len(minterm)*2


def __ack_all_devices_with_different_ack_respect_to_sf(end_devices, transmitters_index):
    logger.info("<ack_all_devices_with_different_ack_respect_to_sf> "
                "Boolean expressions are being created for acking each spreading factor type"
                "end devices ...")
    sf_to_index = __create_sf_to_index_dict(end_devices, transmitters_index)

    Results.SPREADING_FACTOR_BASED_NUMBER_OF_END_DEVICES = {key: len(sf_to_index[key]) for key in sf_to_index}

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


def __create_sf_to_index_dict(end_devices, transmitters_index):
    sf_to_index = {}

    for index in transmitters_index:
        ed = end_devices[index]
        sf_of_ed = getattr(ed, "_sf")

        if sf_to_index.get(sf_of_ed) is None:
            sf_to_index[sf_of_ed] = [index]
        else:
            sf_to_index[sf_of_ed].append(index)

    return sf_to_index
