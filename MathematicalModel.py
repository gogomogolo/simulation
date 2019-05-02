import math
import os
import json


def offeredLoad(slot, iteration, transmissions):
    if iteration == 0:
        attempt = float(transmissions[iteration])
        return attempt / slot
    previousOfferedLoad = float(offeredLoad(slot, iteration - 1, transmissions))
    return (float(slot) * previousOfferedLoad * float(1 - math.exp(-previousOfferedLoad)) + float(
        transmissions[iteration])) / slot


def poisson(slot, iteration, transmissions):
    _offeredLoad = offeredLoad(slot, iteration, transmissions)
    return math.exp(-_offeredLoad)


def totalTransmissionPerAttempt(probOfSucc, iteration, transmissions):
    if iteration == 0:
        return float(transmissions[iteration]) * probOfSucc[iteration]
    return transmissions[iteration] + (1 - probOfSucc[iteration - 1]) * totalTransmissionPerAttempt(probOfSucc,
                                                                                                    iteration - 1,
                                                                                                    transmissions)


def succTranmissionCount(slot, transmissions):
    probOfSucc = [poisson(slot, i, transmissions) for i in range(0, len(transmissions))]
    totalTransmissionsPerAttempt = [totalTransmissionPerAttempt(probOfSucc, i, transmissions) for i in
                                    range(0, len(transmissions))]
    countOfSucc = [probOfSucc[i] * totalTransmissionsPerAttempt[i] for i in range(0, len(probOfSucc))]

    return sum(countOfSucc)


def compareResultWithModel(results_path):
    sfGroupIdPairsShell = "grep \"<Attempt> : 1 |\" " + str(results_path) +"/tasks.subtasks.GroupTransmissionObserver | grep -P \"<SF> : \d+ \| <GroupId> : \d+\" -o"
    sfGroupIdPairs = os.popen(sfGroupIdPairsShell).read().splitlines()

    sfDeviceAmount = {}

    proposedSfSuccTransmitters = {}
    modelSfSuccTransmitters = {}

    proposedSuccTransmitters = 0
    modelSuccTransmitters = 0

    for sfGroupIdPair in sfGroupIdPairs:

        sfGroupIdDeviceAmountShell = "grep " + "\"" + str(
            sfGroupIdPair) + "\" " + str(results_path) + "/tasks.subtasks.GroupTransmissionObserver | grep -P \"<DeviceAmount> : \d+\" -o | awk '{s=$3}END{print s}'"
        sfGroupIdTimeSlotAmountShell = "grep " + "\"" + str(
            sfGroupIdPair) + "\" " + str(results_path) + "/tasks.subtasks.GroupTransmissionObserver | grep -P \"<TimeSlotAmount> : \d+\" -o | awk '{s=$3}END{print s}'"
        sfGroupIdIdleTransmittersAmountShell = "grep " + "\"" + str(
            sfGroupIdPair) + "\" " + str(results_path) + "/tasks.subtasks.GroupTransmissionObserver | grep -P \"<IdleTransmittersAmount> : \d+\" -o | awk '{print $3}'"
        sfGroupIdSuccessfulTransmittersAmountShell = "grep " + "\"" + str(
            sfGroupIdPair) + "\" " + str(results_path) + "/tasks.subtasks.GroupTransmissionObserver | grep -P \"<SuccessfulTransmittersAmount> : \d+\" -o | awk '{s=$3}END{print s}'"

        sfGroupIdDeviceAmount = int(os.popen(sfGroupIdDeviceAmountShell).read())
        sfGroupIdTimeSlotAmount = int(os.popen(sfGroupIdTimeSlotAmountShell).read())
        sfGroupIdSuccessfulTransmittersAmount = int(os.popen(sfGroupIdSuccessfulTransmittersAmountShell).read())
        sfGroupIdIdleTransmittersAmount = list(
            map(int, os.popen(sfGroupIdIdleTransmittersAmountShell).read().splitlines()))

        sfGroupIdIdleTransmittersAmount = [sfGroupIdDeviceAmount] + sfGroupIdIdleTransmittersAmount

        transmissions = [sfGroupIdIdleTransmittersAmount[i - 1] - sfGroupIdIdleTransmittersAmount[i] for i in
                         range(1, len(sfGroupIdIdleTransmittersAmount))]

        succ = succTranmissionCount(sfGroupIdTimeSlotAmount, transmissions)

        proposedSuccTransmitters += sfGroupIdSuccessfulTransmittersAmount
        modelSuccTransmitters += succ

        for sf in range(7, 13):
            query = "<SF> : " + str(sf)
            if query in sfGroupIdPair:
                if sfDeviceAmount.get(sf) is None:
                    sfDeviceAmount[sf] = sfGroupIdDeviceAmount
                    proposedSfSuccTransmitters[sf] = sfGroupIdSuccessfulTransmittersAmount
                    modelSfSuccTransmitters[sf] = succ
                else:
                    sfDeviceAmount[sf] += sfGroupIdDeviceAmount
                    proposedSfSuccTransmitters[sf] += sfGroupIdSuccessfulTransmittersAmount
                    modelSfSuccTransmitters[sf] += succ

    proposedSfSuccProb = {}
    modelSfSuccProb = {}


    allDeviceAmount = 0

    for sf in sfDeviceAmount:
        deviceAmount = sfDeviceAmount.get(sf)
        proposedSfSuccProb[sf] = float(proposedSfSuccTransmitters[sf] / deviceAmount)
        modelSfSuccProb[sf] = float(modelSfSuccTransmitters[sf] / deviceAmount)
        allDeviceAmount += deviceAmount

    proposedSuccProb = float(proposedSuccTransmitters/allDeviceAmount)
    modelSuccProb = float(modelSuccTransmitters / allDeviceAmount)

    result_object = {}
    proposed_object = {}
    model_object = {}

    result_object['DeviceAmount'] = str(allDeviceAmount)
    result_object['SfDeviceAmount'] = str(sfDeviceAmount)

    proposed_object['ProbabilityOfSucc'] = str(proposedSuccProb)
    proposed_object['SfProbabilityOfSucc'] = str(proposedSfSuccProb)
    proposed_object['SfSucceededTransmitters'] = str(proposedSfSuccTransmitters)
    result_object['Proposed'] = proposed_object

    model_object['ProbabilityOfSucc'] = str(modelSuccProb)
    model_object['SfProbabilityOfSucc'] = str(modelSfSuccProb)
    model_object['SfSucceededTransmitters'] = str(modelSfSuccTransmitters)
    result_object['Model'] = model_object

    _r_json = json.dumps(result_object)

    with open(results_path + "/ProposedAndModel", 'a') as the_file:
        the_file.write(_r_json)







