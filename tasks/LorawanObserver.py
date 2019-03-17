import parameters.Constants as Constants
import util.LorawanUtil as LorawanUtil
import util.ProcessUtil as ProcessUtil
import random
from models.CommunicationState import CommunicationState
from models.LorawanResults import LorawanResults


observation_time = 0
observation_start_time = 0
succeeded_communications = []
failed_communications = []
banned_devices = []
failed_devices = []

recursion_count = 0


def start(lorawan_groups):
    global observation_time
    global succeeded_communications
    global banned_devices
    global failed_devices

    observation = True
    observation_time = Constants.SIMULATION_LIFE_TIME_IN_SECONDS
    counter = 0
    previous_observation_time = 0

    while observation:
        if previous_observation_time == observation_time:
            counter += 1
        else:
            counter = 0
        previous_observation_time = observation_time
        lorawan_groups = __communicate(lorawan_groups)
        if counter == 50:
            observation = False

    return LorawanResults([ed for com in succeeded_communications for ed in com.end_devices], failed_devices, banned_devices)


def __communicate(lorawan_groups):
    global observation_start_time
    global observation_time
    global succeeded_communications
    global failed_communications
    global banned_devices
    global failed_devices

    if observation_time <= 0:
        return {}

    communication_history = []
    failed_communications = []

    for sf in lorawan_groups:
        toa = __get_time_on_air(sf)
        devices_of_sf = lorawan_groups.get(sf)
        if observation_time < toa:
            failed_devices += devices_of_sf
            continue
        sf_time_slots_usage = __monitor_resource_usages(toa, devices_of_sf)
        communication_history += [CommunicationState(sf, toa, time_slot, observation_start_time, sf_time_slots_usage.get(time_slot))
                                  for time_slot in sf_time_slots_usage]

    communication_history.sort(key=lambda communication_status: communication_status.first_receive_window_time,
                               reverse=False)

    if communication_history == []:
        return {}

    status_ok_transmissions = __tag_communication_state(communication_history)
    succeeded_communications += status_ok_transmissions

    total_communications_num = len(status_ok_transmissions) + len(failed_communications)

    if total_communications_num == len(communication_history):
        if len(status_ok_transmissions) == len(communication_history):
            lorawan_groups = {}
        else:
            communication_state = communication_history[total_communications_num - 1]

            observation_start_time = communication_state.transmission_time
            observation_time = Constants.SIMULATION_LIFE_TIME_IN_SECONDS - observation_start_time

            lorawan_groups = __create_lorawan_groups(communication_history[total_communications_num:])
    elif 0 < total_communications_num < len(communication_history):
        communication_state = communication_history[total_communications_num]

        observation_start_time = communication_state.transmission_time
        observation_time = Constants.SIMULATION_LIFE_TIME_IN_SECONDS - observation_start_time

        lorawan_groups = __create_lorawan_groups(communication_history[total_communications_num:])

    elif 0 == total_communications_num:
        lorawan_groups = {}

    return lorawan_groups


def __create_lorawan_groups(communication_history):
    global failed_communications
    global banned_devices

    lorawan_groups = {}

    for failed_communication in failed_communications:
        sf = failed_communication.sf
        end_devices = failed_communication.end_devices

        for end_device in end_devices:
            end_device.increment_retransmission_attempt_count()
            if end_device.is_banned():
                banned_devices.append(end_device)
            else:
                if lorawan_groups.get(sf) is None:
                    lorawan_groups[sf] = [end_device]
                else:
                    lorawan_groups[sf].append(end_device)

    for communication_state in communication_history:
        sf = communication_state.sf

        if lorawan_groups.get(sf) is None:
            lorawan_groups[sf] = communication_state.end_devices
        else:
            lorawan_groups[sf] += communication_state.end_devices

    return lorawan_groups


def __monitor_resource_usages(toa, lorawan_sf_devices):
    used_resources = __find_used_time_slots(toa, lorawan_sf_devices)
    active_transmitters = __find_active_transmitters(lorawan_sf_devices)
    resource_usage = __compose_resource_usages(used_resources, active_transmitters)
    return resource_usage


def __find_used_time_slots(toa, lorawan_sf_devices):
    global observation_time

    time_slots = []
    lorawan_sf_devices_count = len(lorawan_sf_devices)
    time_slot_number = int(observation_time/toa)
    active_transmitters_count = lorawan_sf_devices_count
    for i in range(0, active_transmitters_count):
        time_slots.append(random.randint(0, time_slot_number - 1))
    return time_slots


def __find_active_transmitters(lorawan_sf_devices):
    lorawan_sf_devices_count = len(lorawan_sf_devices)
    active_transmitters_amount = lorawan_sf_devices_count
    active_transmitters_indexes = \
        __select_active_transmitters_index(active_transmitters_amount, lorawan_sf_devices_count)
    active_transmitters = []
    for index in active_transmitters_indexes:
        active_transmitters.append(lorawan_sf_devices.pop(index))

    return active_transmitters


def __select_active_transmitters_index(active_transmitters_amount, lorawan_sf_devices_count):
    _random = random.Random()
    seed = _random.randint(1, 30000)
    _random.seed(seed)
    indexes = _random.sample(range(0, lorawan_sf_devices_count), active_transmitters_amount)
    indexes.sort(reverse=True)
    return indexes


def __compose_resource_usages(used_resources, active_transmitters):
    resource_usages = {}
    for index in range(0, len(used_resources)):
        if resource_usages.get(used_resources[index]) is None:
            resource_usages[used_resources[index]] = [active_transmitters[index]]
        else:
            resource_usages[used_resources[index]].append(active_transmitters[index])
    return resource_usages


def __tag_communication_state(communication_history):
    gateway_active_timestamp = 0
    gateway_passive_timestamp = 0

    gateway_transmission_start_time = 0
    gateway_transmission_end_time = 0

    global failed_communications

    failed_communications = []

    ok = []

    first_failed_transmission_detector = False
    succeeded_transmission_after_first_failure = False

    for communication_status in communication_history:
        if communication_status.is_collision is True:
            if first_failed_transmission_detector is not True:
                first_failed_transmission_detector = True
            failed_communications.append(communication_status)

        else:
            # Communication channel is bidirectional so if there is an UL channel between gw and ed,
            # DL channel should not be connected between them or vice versa.
            if __channel_transmission_state(gateway_transmission_start_time,
                                            gateway_transmission_end_time,
                                            communication_status.transmission_time) \
                    == "DL_ACTIVE_UL_CONTROL_NEEDLESS":
                if first_failed_transmission_detector is not True:
                    first_failed_transmission_detector = True
                failed_communications.append(communication_status)

            elif __channel_transmission_state(gateway_transmission_start_time,
                                              gateway_transmission_end_time,
                                              communication_status.transmission_time) \
                    == "DL_WILL_BE_ACTIVE_UL_CONTROL_NEEDED":
                if communication_status.end_of_transmission_time >= gateway_transmission_start_time:
                    if first_failed_transmission_detector is not True:
                        first_failed_transmission_detector = True
                    failed_communications.append(communication_status)
                else:
                    if gateway_transmission_start_time <= communication_status.first_receive_window_time <= gateway_transmission_end_time:
                        receiving_message_end_time = communication_status.first_receive_window_time + communication_status.receiving_message_toa
                        if receiving_message_end_time > gateway_transmission_end_time:
                            gateway_transmission_end_time = receiving_message_end_time

                            gateway_transmission_duration_time = gateway_transmission_end_time - gateway_transmission_start_time

                            gateway_passive_timestamp = gateway_transmission_end_time
                            gateway_active_timestamp = gateway_transmission_start_time + \
                                                       (gateway_transmission_duration_time * float(
                                                           100 / Constants.DUTY_CYCLE_IN_PERCENTAGE))
                        if first_failed_transmission_detector is True:
                            succeeded_transmission_after_first_failure = True
                        if succeeded_transmission_after_first_failure is not True:
                            ok.append(communication_status)
                    else:
                        if first_failed_transmission_detector is not True:
                            first_failed_transmission_detector = True
                        failed_communications.append(communication_status)

            elif __channel_transmission_state(gateway_transmission_start_time,
                                              gateway_transmission_end_time,
                                              communication_status.transmission_time) \
                    == "DL_PASSIVE_DL_DUTY_CYCLE_CONTROL_NEEDED":
                if gateway_passive_timestamp < communication_status.second_receive_window_time < gateway_active_timestamp:
                    if first_failed_transmission_detector is not True:
                        first_failed_transmission_detector = True
                    failed_communications.append(communication_status)
                else:
                    if communication_status.first_receive_window_time > gateway_active_timestamp:
                        gateway_transmission_start_time = communication_status.first_receive_window_time
                    else:
                        gateway_transmission_start_time = communication_status.second_receive_window_time

                    gateway_transmission_end_time = gateway_transmission_start_time + communication_status.receiving_message_toa

                    gateway_passive_timestamp = gateway_transmission_end_time
                    gateway_active_timestamp = gateway_transmission_start_time + \
                                               (communication_status.receiving_message_toa * float(
                                                   100 / Constants.DUTY_CYCLE_IN_PERCENTAGE))
                    if first_failed_transmission_detector is True:
                        succeeded_transmission_after_first_failure = True
                    if succeeded_transmission_after_first_failure is not True:
                        ok.append(communication_status)

        if succeeded_transmission_after_first_failure is True:
            break

    return ok


def __channel_transmission_state(gw_tstart_t, gw_tend_t, ed_tstart_t):

    if gw_tstart_t <= ed_tstart_t <= gw_tend_t:
        ed_ts = "DL_ACTIVE_UL_CONTROL_NEEDLESS"
    elif ed_tstart_t < gw_tstart_t:
        ed_ts = "DL_WILL_BE_ACTIVE_UL_CONTROL_NEEDED"
    elif gw_tend_t < ed_tstart_t:
        ed_ts = "DL_PASSIVE_DL_DUTY_CYCLE_CONTROL_NEEDED"
    return ed_ts


def __find_time_slot(time_offset, time_period, time_on_air):
    return float(time_offset+time_period)/time_on_air


def __get_time_on_air(sf):
    return LorawanUtil.calculate_time_on_air(
            Constants.BANDWIDTH_IN_HERTZ,
            Constants.NUMBER_OF_PREAMBLE,
            Constants.SYNCHRONIZATION_WORD,
            Constants.SF_TO_MAC_PAYLOAD_IN_BYTE[sf],
            sf,
            Constants.CRC,
            Constants.IH,
            Constants.DE,
            Constants.CODING_RATE)