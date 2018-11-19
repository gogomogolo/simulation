import parameters.Results as Results
import parameters.Constants as Constants
import time
import os
import numpy as np
import matplotlib.pyplot as plt


def prepare_statistics():
    dir_name = os.path.abspath(os.path.join('results',time.strftime("%Y%m%d-%H%M%S")))
    os.makedirs(dir_name)
    observation_groups = getattr(Results.SIMULATION_RESULT, "_SimulationResult__observation_groups")
    for observation_group in observation_groups:
        spreading_factor = getattr(observation_group, "_ObservationGroup__sf")
        lifecycles = getattr(observation_group, "_ObservationGroup__lifecycles")
        #sketch_transmission_state_rate_to_lifecycle(spreading_factor, lifecycles, dir_name)
        sketch_payload_of_ack_to_group_id(spreading_factor, lifecycles, dir_name)


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
    bar_width = 0.1
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
    plt.savefig(os.path.join(dir_name, 'SF_' + str(sf) + '_' + time.strftime("%Y%m%d-%H%M%S") + '.png'))
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
    plt.savefig(os.path.join(dir_name, 'SF_' + str(sf) + '_' + time.strftime("%Y%m%d-%H%M%S") + '.png'))
    plt.clf()

