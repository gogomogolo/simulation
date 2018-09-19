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


formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')
screen_handler = logging.StreamHandler(stream=sys.stdout)
screen_handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(screen_handler)
logger.setLevel(logging.DEBUG)


def run():
    logger.info("<run> Simulation is starting...")

    exponential_size = Constants.EXPONENTIAL_DIST_SIZE
    exponential_scale = Constants.EXPONENTIAL_DIST_SCALE
    exponential = Exponential(exponential_size, exponential_scale)

    end_devices = distribute(exponential)
    super_group = SuperGroupGenerator.generate(end_devices)

    group_id_to_finalized_observers = __play_aggregated_acknowledge_scenario(super_group)
    group_id_to_acknowledgement = __create_acknowledgement_for_group(group_id_to_finalized_observers)
    group_id_to_sf_acknowledgement = __create_acknowledgement_for_group_in_detail_of_sf(group_id_to_finalized_observers)
    Results.GROUP_ID_TO_ACKNOWLEDGEMENT = group_id_to_acknowledgement
    Results.GROUP_ID_TO_SF_ACKNOWLEDGEMENT = group_id_to_sf_acknowledgement


def __play_aggregated_acknowledge_scenario(super_group):
    group_id_to_finalized_observers = {}

    for group in super_group:
        total_thread_count = __calculate_total_thread_count(group)
        barrier = threading.Barrier(total_thread_count)

        transmission_observers = UplinkTransmissionObserverGenerator.generate(group, barrier)

        for transmission_observer in transmission_observers:
            transmission_observer.start()

        barrier.wait()

        group_id_to_finalized_observers[getattr(group, '__id')] = transmission_observers

    return group_id_to_finalized_observers


def __create_acknowledgement_for_group(groupid_to_observers):
    groupid_to_acknowledgement = {}

    for group_id in groupid_to_observers:
        successful_transmitters = getattr(groupid_to_observers[group_id], '__end_devices_success_transmission')
        end_device_ids = \
            [int(getattr(end_device, '_id')[:(len(getattr(end_device, '_id'))-len(group_id))], base=2)
             for end_device in successful_transmitters]
        qmc = QMC(end_device_ids)
        groupid_to_acknowledgement[group_id] = qmc.minimize()

    return groupid_to_acknowledgement


def __create_acknowledgement_for_group_in_detail_of_sf(groupid_to_observers):
    groupid_to_sf_acknowledgement = {}

    for group_id in groupid_to_observers:
        observers = groupid_to_observers[group_id]
        sf_to_end_devices = \
            {getattr(observer, '__sf'): getattr(observer, '__end_devices_success_transmission')
             for observer in observers}
        sf_to_acknowledgement = {}
        for sf in sf_to_end_devices:
            end_device_ids = \
                [int(getattr(end_device, '_id')[:(len(getattr(end_device, '_id'))-len(group_id))], base=2)
                 for end_device in sf_to_end_devices[sf]]
            qmc = QMC(end_device_ids)
            sf_to_acknowledgement[sf] = qmc.minimize()

        groupid_to_sf_acknowledgement[group_id] = sf_to_acknowledgement

    return groupid_to_sf_acknowledgement


def __calculate_total_thread_count(group):
    sf_to_end_devices = getattr(group, '__sf_to_end_devices')
    return len(sf_to_end_devices) + 1

