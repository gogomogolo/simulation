import parameters.Results as Results
import time
import os
import numpy as np
import matplotlib.pyplot as plt
import util.LogUtil as LogUtil
import parameters.Constants as Constants


def prepare_statistics():
    dir_name = os.path.abspath(os.path.join('results',time.strftime("%Y%m%d-%H%M%S")))
    os.makedirs(dir_name)
    observation_groups = getattr(Results.SIMULATION_RESULT, "_SimulationResult__observation_groups")
    for observation_group in observation_groups:
        spreading_factor = getattr(observation_group, "_ObservationGroup__sf")
        lifecycles = getattr(observation_group, "_ObservationGroup__lifecycles")
        sketch_transmission_state_rate_to_lifecycle(spreading_factor, lifecycles, dir_name)
        sketch_payload_of_ack_to_group_id(spreading_factor, lifecycles, dir_name)
        sketch_status_of_time_slots(spreading_factor, lifecycles, dir_name)
        sketch_end_device_num_of_time_slots(spreading_factor, lifecycles, dir_name)

    for super_group in Results.SUPER_GROUPS:
        sketch_time_slot_number_to_group_id(super_group, dir_name)
        sketch_device_number_to_group_id(super_group, dir_name)


def sketch_device_number_to_group_id(super_group, dir_name):
    sf = getattr(super_group, "_SuperGroup__sf")
    groups = getattr(super_group, "_SuperGroup__groups")

    gid_x_axis = [getattr(group, "_Group__id") for group in groups]
    device_num_y_axis = ()

    for group in groups:
        device_num_y_axis = device_num_y_axis + (len(getattr(group, "_Group__end_devices")),)

    plt.plot()
    index = np.arange(len(gid_x_axis))
    bar_width = 0.50
    opacity = 0.8

    rects1 = plt.bar(index, device_num_y_axis, bar_width,
                     alpha=opacity,
                     color='g',
                     label='GroupId Device Num')

    plt.xlabel('Group Id')
    plt.ylabel('Device Number')
    plt.title('Spreading Factor: ' + str(sf))
    plt.xticks(index + bar_width, gid_x_axis)
    plt.legend()

    plt.tight_layout()
    plt.savefig(os.path.join(dir_name, 'Device_Num_SF_' + str(sf) + '_' + time.strftime("%Y%m%d-%H%M%S") + '.png'))
    plt.gcf().clear()
    plt.clf()


def sketch_time_slot_number_to_group_id(super_group, dir_name):
    sf = getattr(super_group, "_SuperGroup__sf")
    groups = getattr(super_group, "_SuperGroup__groups")

    gid_x_axis = [getattr(group, "_Group__id") for group in groups]
    time_slot_num_y_axis = ()

    for group in groups:
        time_slot_num_y_axis = time_slot_num_y_axis + (getattr(group, "_Group__time_slot_number"),)

    plt.plot()
    index = np.arange(len(gid_x_axis))
    bar_width = 0.50
    opacity = 0.8

    rects1 = plt.bar(index, time_slot_num_y_axis, bar_width,
                     alpha=opacity,
                     color='g',
                     label='GroupId Time Slot')

    plt.xlabel('Group Id')
    plt.ylabel('Time Slot Number')
    plt.title('Spreading Factor: ' + str(sf))
    plt.xticks(index + bar_width, gid_x_axis)
    plt.legend()

    plt.tight_layout()
    plt.savefig(os.path.join(dir_name, 'Time_Slot_SF_' + str(sf) + '_' + time.strftime("%Y%m%d-%H%M%S") + '.png'))
    plt.gcf().clear()
    plt.clf()


def sketch_status_of_time_slots(sf, lifecycles, dir_name):
    gid_tss = {}

    for lifecycle_group in lifecycles:
        gid_tss = getattr(lifecycle_group, "_LifecycleGroup__group_id_to_time_slot_status")
        break

    group_ids = list(gid_tss.keys())

    for group_id in group_ids:
        gid = str(group_id)
        time_slot_to_status = gid_tss[group_id]

        x_axis = tuple(list(time_slot_to_status.keys()))
        slots_status = time_slot_to_status.values()
        y_axis = ()

        for status in slots_status:
            y_axis = y_axis + (status,)

        plt.plot()
        index = np.arange(len(x_axis))
        bar_width = 0.5
        opacity = 0.8

        rects1 = plt.bar(index, y_axis, bar_width,
                         alpha=opacity,
                         color='g',
                         label='TimeSlot State')

        plt.xlabel('Time Slot')
        plt.ylabel('State')
        plt.title('Spreading Factor: ' + str(sf))
        plt.xticks(index + bar_width, x_axis)
        plt.legend()

        plt.tight_layout()
        plt.savefig(os.path.join(dir_name, 'Status_SF_' + str(sf) + '_GID_' + gid + '_' + time.strftime("%Y%m%d-%H%M%S") + '.png'))
        plt.gcf().clear()
        plt.clf()


def sketch_end_device_num_of_time_slots(sf, lifecycles, dir_name):
    gid_tss = {}

    for lifecycle_group in lifecycles:
        gid_tss = getattr(lifecycle_group, "_LifecycleGroup__group_id_to_time_slot_statistics")
        break

    group_ids = list(gid_tss.keys())

    for group_id in group_ids:
        gid = str(group_id)
        time_slot_to_status = gid_tss[group_id]

        x_axis = tuple(list(time_slot_to_status.keys()))
        slots_stat = time_slot_to_status.values()
        y_axis = ()

        for stat in slots_stat:
            y_axis = y_axis + (stat,)

        plt.plot()
        index = np.arange(len(x_axis))
        bar_width = 0.5
        opacity = 0.8

        rects1 = plt.bar(index, y_axis, bar_width,
                         alpha=opacity,
                         color='g',
                         label='TimeSlot EndDeviceNum')

        plt.xlabel('Time Slot')
        plt.ylabel('EndDevice Number')
        plt.title('Spreading Factor: ' + str(sf))
        plt.xticks(index + bar_width, x_axis)
        plt.legend()

        plt.tight_layout()
        plt.savefig(os.path.join(dir_name, 'EndDevice_SF_' + str(sf) + '_GID_' + gid + '_' + time.strftime("%Y%m%d-%H%M%S") + '.png'))
        plt.gcf().clear()
        plt.clf()

def sketch_payload_of_ack_to_group_id(sf, lifecycles, dir_name):
    for lifecycle_group in lifecycles:
        lifecycle = getattr(lifecycle_group, "_LifecycleGroup__cycle")
        gid_ack = getattr(lifecycle_group, "_LifecycleGroup__group_id_to_aggregated_acknowledgement")
        break

    gid_axis = tuple(list(gid_ack.keys()))
    acks = gid_ack.values()
    payload_in_byte_axis = ()
    for ack in acks:
        if ack is None:
            payload_in_byte_axis = payload_in_byte_axis + (0,)
        else:
            payload_in_byte_axis = payload_in_byte_axis + ((len(list(ack))*len(list(ack)[0]))/4,)

    plt.plot()
    index = np.arange(len(gid_axis))
    bar_width = 0.5
    opacity = 0.8

    rects1 = plt.bar(index, payload_in_byte_axis, bar_width,
                     alpha=opacity,
                     color='g',
                     label='Groupıd Payload')

    plt.xlabel('Group Id')
    plt.ylabel('Ack Payload in Byte')
    plt.title('Spreading Factor: ' + str(sf))
    plt.xticks(index + bar_width, gid_axis)
    plt.legend()

    plt.tight_layout()
    plt.savefig(os.path.join(dir_name, 'Payload_SF_' + str(sf) + '_' + time.strftime("%Y%m%d-%H%M%S") + '.png'))
    plt.gcf().clear()
    plt.clf()


def sketch_transmission_state_rate_to_lifecycle(sf, lifecycles, dir_name):
    cycle_count = len(lifecycles)
    lf_axis = ()
    suc_bar = ()
    fail_bar = ()
    sus_bar = ()
    for lifecycle_group in lifecycles:
        lifecycle = getattr(lifecycle_group, "_LifecycleGroup__cycle")
        gid_ack = getattr(lifecycle_group, "_LifecycleGroup__group_id_to_aggregated_acknowledgement")
        gid_suc = getattr(lifecycle_group, "_LifecycleGroup__group_id_to_successful_transmissions")
        gid_fail = getattr(lifecycle_group, "_LifecycleGroup__group_id_to_failed_transmissions")
        gid_sus = getattr(lifecycle_group, "_LifecycleGroup__group_id_to_suspended_transmissions")

        sum_suc = sum(gid_suc.values())
        sum_fail = sum(gid_fail.values())
        sum_sus = sum(gid_sus.values())

        sum_all = sum_suc + sum_fail + sum_sus

        lf_axis = lf_axis + (str(lifecycle+1),)
        suc_bar = suc_bar + (float(sum_suc)/sum_all,)
        fail_bar = fail_bar + (float(sum_fail)/sum_all,)
        sus_bar = sus_bar + (float(sum_sus)/sum_all,)

    plt.plot()
    index = np.arange(cycle_count)
    bar_width = 0.01
    opacity = 0.8

    rects1 = plt.bar(index, suc_bar, bar_width,
                     alpha=opacity,
                     color='g',
                     label='Successful Transmission Rate')

    rects2 = plt.bar(index + bar_width, fail_bar, bar_width,
                     alpha=opacity,
                     color='r',
                     label='Failed Transmission Rate')

    rects3 = plt.bar(index + bar_width + bar_width, sus_bar, bar_width,
                     alpha=opacity,
                     color='b',
                     label='Suspended Transmission Rate')

    plt.xlabel('Life cycle')
    plt.ylabel('Transmissions State Rate')
    plt.title('Spreading Factor: ' + str(sf))
    plt.xticks(index + bar_width, lf_axis)
    plt.legend()

    plt.tight_layout()
    plt.savefig(os.path.join(dir_name, 'State_SF_' + str(sf) + '_' + time.strftime("%Y%m%d-%H%M%S") + '.png'))
    plt.gcf().clear()
    plt.clf()


def flush():
    observation_groups = getattr(Results.SIMULATION_RESULT, "_SimulationResult__observation_groups")
    for observation_group in observation_groups:
        spreading_factor = getattr(observation_group, "_ObservationGroup__sf")
        lifecycles = getattr(observation_group, "_ObservationGroup__lifecycles")
        for lifecycle_group in lifecycles:
            lifecycle = getattr(lifecycle_group, "_AttemptSuperGroup__cycle")
            gid_ack_wo_bexpr = getattr(lifecycle_group,
                              "_AttemptSuperGroup__group_id_to_aggregated_acknowledgement_without_bexpr")
            gid_ack_w_bexpr = getattr(lifecycle_group,
                              "_AttemptSuperGroup__group_id_to_aggregated_acknowledgement_with_bexpr")
            gid_tc = getattr(lifecycle_group, "_AttemptSuperGroup__group_id_to_transmission_count")
            for gid in gid_ack_w_bexpr:
                tc = gid_tc[gid]

                ack_w_bexpr = gid_ack_w_bexpr[gid]
                payload_in_byte_w_bexpr = 0
                message_in_byte_w_bexpr = 0
                if ack_w_bexpr is not None:
                    payload_in_byte_w_bexpr = (len(list(ack_w_bexpr)*len(list(ack_w_bexpr)[0]))/4)
                    if payload_in_byte_w_bexpr != 0:
                        message_in_byte_w_bexpr = 13 + payload_in_byte_w_bexpr

                ack_wo_bexpr = gid_ack_wo_bexpr[gid]
                payload_in_byte_wo_bexpr = 0
                message_in_byte_wo_bexpr = 0
                if ack_wo_bexpr is not None:
                    payload_in_byte_wo_bexpr = len(list(ack_wo_bexpr)*len(list(ack_wo_bexpr)[0]))/8
                    if payload_in_byte_wo_bexpr != 0:
                        message_in_byte_wo_bexpr = 13 + payload_in_byte_wo_bexpr

                LogUtil.get_file_logger(__name__).info(
                    "| <Attempt> : %s | <SF> : %s | <GroupId> : %s "
                    "| <MacPayloadByteWithExpressionSolution> : %s | <MacPayloadByteWithStandardSolution> : %s "
                    "| <MaxBoundaryMacPayload> : %s "
                    "| <DLMessageSizeByteWithExpressionSolution> : %s | <DLMessageSizeByteWithStandardSolution> : %s "
                    "| <TotalULTransmission> : %s "
                    "| <TotalULMessageSizeByte> : %s |",
                    str(lifecycle+1), str(spreading_factor), str(gid),
                    str(payload_in_byte_w_bexpr), str(payload_in_byte_wo_bexpr),
                    str(Constants.SF_TO_MAX_MAC_PAYLOAD_IN_BYTE[spreading_factor]),
                    str(message_in_byte_w_bexpr), str(message_in_byte_wo_bexpr),
                    str(tc), str(tc*(13+Constants.SF_TO_MAC_PAYLOAD_IN_BYTE[spreading_factor])))

def networkLoad(results_path):
    observation_groups = getattr(Results.SIMULATION_RESULT, "_SimulationResult__observation_groups")
    for observation_group in observation_groups:
        sfgid_cycles_tc = {}
        sfgid_cycles_stc = {}
        spreading_factor = getattr(observation_group, "_ObservationGroup__sf")
        lifecycles = getattr(observation_group, "_ObservationGroup__lifecycles")
        for lifecycle_group in lifecycles:
            lifecycle = getattr(lifecycle_group, "_AttemptSuperGroup__cycle")
            gid_tc = getattr(lifecycle_group, "_AttemptSuperGroup__group_id_to_transmission_count")
            gid_stc = getattr(lifecycle_group, "_AttemptSuperGroup__group_id_to_successful_transmissions_not_cumulative")
            for gid in gid_tc:
                tag = str(spreading_factor) + "|" + str(gid)
                if sfgid_cycles_tc.get(tag) is None:
                    sfgid_cycles_tc[tag] = [gid_tc.get(gid)]
                    sfgid_cycles_stc[tag] = [gid_stc.get(gid)]
                else:
                    sfgid_cycles_tc[tag].append(gid_tc.get(gid))
                    sfgid_cycles_stc[tag].append(gid_stc.get(gid))
        with open(results_path + "/proposedsfidattemptpos", 'a') as the_file:
            for sfgid in sfgid_cycles_tc:
                the_file.write(str(sfgid) + " : " + str(sfgid_cycles_stc.get(sfgid)) + str('\n'))
                the_file.write(str(sfgid) + " : " + str(sfgid_cycles_tc.get(sfgid))+ str('\n'))