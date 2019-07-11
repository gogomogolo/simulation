import Simulation as sim
import MatlabInputFileCreator as mtlbio
import json
import ast

OCCURRENCE_OF_SIM = 15
SIMULATION_LIFE_TIME_IN_SECONDS = 86400
SF_TO_SUPER_GROUP_PERIOD_IN_SEC = {7: 3600, 8: 3600, 9: 3600, 10: 3600, 11: 3600, 12: 3600}


def autorun1():
    SF_TO_MAC_PAYLOAD_IN_BYTEs = {'Min': {7: 10, 8: 10, 9: 10, 10: 10, 11: 10, 12: 10}}
    END_DEVICE_NUMBERs = [1000, 2500, 5000, 7500, 10000]

    occurrence_history = {}

    for occ in range(1, OCCURRENCE_OF_SIM+1):
        device_history = {}
        for edn in END_DEVICE_NUMBERs:
            payloadtype_history = {}
            for pt in SF_TO_MAC_PAYLOAD_IN_BYTEs:
                sim_res_dir = sim.simulation(SF_TO_MAC_PAYLOAD_IN_BYTEs[pt], edn, SF_TO_SUPER_GROUP_PERIOD_IN_SEC, SIMULATION_LIFE_TIME_IN_SECONDS)
                payloadtype_history[pt] = sim_res_dir
            device_history[edn] = payloadtype_history
        occurrence_history[occ] = device_history

    _r_json = json.dumps(occurrence_history)

    with open("autorun1", 'a') as the_file:
        the_file.write(_r_json)

    mtlbio.minPayloadAllDevicePoSCSVCreate(occurrence_history, END_DEVICE_NUMBERs)

def autorun2():
    SF_TO_MAC_PAYLOAD_IN_BYTEs = {
        'Min': {7: 10, 8: 10, 9: 10, 10: 10, 11: 10, 12: 10},
        'Avg': {7: 125, 8: 125, 9: 60, 10: 30, 11: 30, 12: 30},
        'Max': {7: 250, 8: 250, 9: 123, 10: 59, 11: 59, 12: 59}
    }
    END_DEVICE_NUMBERs = [5000]

    occurrence_history = {}

    for occ in range(1, OCCURRENCE_OF_SIM+1):
        device_history = {}
        for edn in END_DEVICE_NUMBERs:
            payloadtype_history = {}
            for pt in SF_TO_MAC_PAYLOAD_IN_BYTEs:
                sim_res_dir = sim.simulation(SF_TO_MAC_PAYLOAD_IN_BYTEs[pt], edn, SF_TO_SUPER_GROUP_PERIOD_IN_SEC, SIMULATION_LIFE_TIME_IN_SECONDS)
                payloadtype_history[pt] = sim_res_dir
            device_history[edn] = payloadtype_history
        occurrence_history[occ] = device_history

    _r_json = json.dumps(occurrence_history)

    pts = ['Min', 'Avg', 'Max']

    with open("autorun2", 'a') as the_file:
        the_file.write(_r_json)

    mtlbio.fivethsndDeviceAllPayloadTypePoSCSVCreate(occurrence_history, pts)


def autorun1_continue(endDeviceCaseMethod):
    with open("autorun1") as state_file:
        content = state_file.readlines()
        content = [x.strip() for x in content]

    occurrence_history = ast.literal_eval(content[0])

    END_DEVICE_NUMBERs = [1000, 2500, 5000, 7500, 10000]

    endDeviceCaseMethod(occurrence_history, END_DEVICE_NUMBERs)

def autorun2_continue(payloadTypeCaseMethod):
    with open("autorun2") as state_file:
        content = state_file.readlines()
        content = [x.strip() for x in content]

    occurrence_history = ast.literal_eval(content[0])

    pts = ['Min', 'Avg', 'Max']

    payloadTypeCaseMethod(occurrence_history, pts)


try:
    autorun1_continue(mtlbio.performanceMetricsDeviceNumberCase)
except:
    print("autorun1 file does not esixt")


try:
    autorun2_continue(mtlbio.performanceMetricsPayloadTypeCase)
except:
    print("autorun2 file does not esixt")
