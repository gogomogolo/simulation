import parameters.Constants as Constants
import parameters.Results as Results
import logging
import sys
import generators.SuperGroupObserverGenerator as SuperGroupObserverGenerator
import generators.LorawanGroupGenerator as LorawanGroupGenerator
import generators.SuperGroupGenerator as SuperGroupGenerator
import generators.EndDeviceDistributor as EndDeviceDistributor
import generators.SimulationResultGenerator as SimulationResultGenerator
import tasks.LorawanObserver as LorawanObserver
import threading

from distributions.Exponential import Exponential


formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')
screen_handler = logging.StreamHandler(stream=sys.stdout)
screen_handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(screen_handler)
logger.setLevel(logging.DEBUG)


def run():
    logger.info("<run> Simulation is starting...")

    end_devices = create_end_devices()

    run_lorawan_solution(end_devices)

    run_proposed_solution(end_devices)

    logger.info("<run> Simulation is ending...")


def create_end_devices():
    exponential_size = Constants.EXPONENTIAL_DIST_SIZE
    exponential_scale = Constants.EXPONENTIAL_DIST_SCALE
    exponential = Exponential(exponential_size, exponential_scale)

    return EndDeviceDistributor.distribute(exponential)


def run_proposed_solution(end_devices):
    super_groups = SuperGroupGenerator.generate(end_devices)
    Results.SUPER_GROUPS = super_groups

    super_group_observers = __play_aggregated_acknowledge_scenario(super_groups)
    Results.SIMULATION_RESULT = __create_simulation_result(super_group_observers)


def run_lorawan_solution(end_devices):
    lorawan_groups = LorawanGroupGenerator.generate(end_devices)

    LorawanObserver.start(lorawan_groups)


def __play_aggregated_acknowledge_scenario(super_groups):
    total_thread_count = __calculate_total_thread_count(super_groups)
    barrier = threading.Barrier(total_thread_count)

    super_group_observers = \
        [SuperGroupObserverGenerator.generate(super_group, barrier) for super_group in super_groups]

    for super_group_observer in super_group_observers:
        super_group_observer.start()

    barrier.wait()

    return super_group_observers


def __create_simulation_result(super_group_observers):
    return SimulationResultGenerator.generate(super_group_observers)


def __calculate_total_thread_count(super_groups):
    return len(super_groups) + 1

