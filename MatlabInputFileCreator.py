import json
import ast
from collections import namedtuple, Counter


def filecreate(sim_occurrence_history, edns, pts):
    minPayloadAllDevicePoSCSVCreate(sim_occurrence_history, edns)
    fivethsndDeviceAllPayloadTypePoSCSVCreate(sim_occurrence_history, pts)


def fivethsndDeviceAllPayloadTypePoSCSVCreate(sim_occurrence_history, pts):
    _pt = {'Min': 1, 'Max': 3, 'Avg': 2}
    edn = 5000

    occurrence_count = len(sim_occurrence_history)

    csvAllSf = ["payloadType, PS-PoS, PM-PoS, PA-PoS"]
    csvLabelSeparatedSf = [
        "payloadType, SF7-PS-PoS, SF7-PM-PoS, SF7-PA-PoS, SF8-PS-PoS, SF8-PM-PoS, SF8-PA-PoS, SF9-PS-PoS, SF9-PM-PoS, SF9-PA-PoS, SF10-PS-PoS, SF10-PM-PoS, SF10-PA-PoS, SF11-PS-PoS, SF11-PM-PoS, SF11-PA-PoS, SF12-PS-PoS, SF12-PM-PoS, SF12-PA-PoS "]

    pandm = "/ProposedAndModel"
    lrwnpa = "/LorawanPureAloha"

    for pt in pts:
        ps_pos = 0.0
        pm_pos = 0.0
        pa_pos = 0.0
        for occ in sim_occurrence_history:
            sim_res_dir = sim_occurrence_history[occ][edn][pt]

            with open(sim_res_dir + lrwnpa) as lrwnpa_f:
                lrwnpa_content = lrwnpa_f.readlines()
            lrwnpa_content = [x.strip() for x in lrwnpa_content]

            with open(sim_res_dir + pandm) as pandm_f:
                pandm_content = pandm_f.readlines()
            pandm_content = [x.strip() for x in pandm_content]

            pandm_json_r = json2obj(pandm_content[0])
            lrwnpa_json_r = json2obj(lrwnpa_content[0])

            ps_pos += float(pandm_json_r.Proposed.ProbabilityOfSucc)
            pm_pos += float(pandm_json_r.Model.ProbabilityOfSucc)
            pa_pos += float(lrwnpa_json_r.SuccXmt) / edn
        ps_pos /= float(occurrence_count)
        pm_pos /= float(occurrence_count)
        pa_pos /= float(occurrence_count)
        csvAllSf.append(str(_pt[pt]) + ", " + str(ps_pos) + ", " + str(pm_pos) + ", " + str(pa_pos))

    with open('fivethsndDeviceAllPayloadTypePoS.csv', 'a') as fivethsndDeviceAllPayloadTypePoS:
        for line in csvAllSf:
            fivethsndDeviceAllPayloadTypePoS.write(line + '\n')

    for pt in pts:
        sf_ps_pos = {}
        sf_pm_pos = {}
        sf_pa_pos = {}

        for occ in sim_occurrence_history:
            sim_res_dir = sim_occurrence_history[occ][edn][pt]

            with open(sim_res_dir + lrwnpa) as lrwnpa_f:
                lrwnpa_content = lrwnpa_f.readlines()
            lrwnpa_content = [x.strip() for x in lrwnpa_content]

            with open(sim_res_dir + pandm) as pandm_f:
                pandm_content = pandm_f.readlines()
            pandm_content = [x.strip() for x in pandm_content]

            pandm_json_r = json2obj(pandm_content[0])
            lrwnpa_json_r = json2obj(lrwnpa_content[0])

            proposed_sf_pos = ast.literal_eval(pandm_json_r.Proposed.SfProbabilityOfSucc)
            model_sf_pos = ast.literal_eval(pandm_json_r.Model.SfProbabilityOfSucc)
            lrwnpa_sf_pos = ast.literal_eval(lrwnpa_json_r.SfSuccXmt)
            sf_device_amount = ast.literal_eval(pandm_json_r.SfDeviceAmount)

            sf_ps_pos = dict(Counter(sf_ps_pos) + Counter(proposed_sf_pos))
            sf_pm_pos = dict(Counter(sf_pm_pos) + Counter(model_sf_pos))
            sf_pa_pos = dict(Counter(sf_pa_pos) + Counter(
                {sf: float(lrwnpa_sf_pos[sf]) / sf_device_amount[sf] for sf in lrwnpa_sf_pos}))

        sf_ps_pos = {sf: sf_ps_pos[sf] / float(occurrence_count) for sf in sf_ps_pos}
        sf_pm_pos = {sf: sf_pm_pos[sf] / float(occurrence_count) for sf in sf_pm_pos}
        sf_pa_pos = {sf: sf_pa_pos[sf] / float(occurrence_count) for sf in sf_pa_pos}

        line = ""
        for sf in sf_ps_pos:
            line += ", " + str(sf_ps_pos[sf]) + ", " + str(sf_pm_pos[sf]) + ", " + str(sf_pa_pos[sf])
        csvLabelSeparatedSf.append(str(_pt[pt]) + line)

    with open('fivethsndDeviceSFAllPayloadTypePoS.csv', 'a') as fivethsndDeviceSFAllPayloadTypePoS:
        for line in csvLabelSeparatedSf:
            fivethsndDeviceSFAllPayloadTypePoS.write(line + '\n')

def minPayloadAllDevicePoSCSVCreate(sim_occurrence_history, edns):
    pt = 'Min'
    occurrence_count = len(sim_occurrence_history)

    csvAllSf = ["nodeCount, PS-PoS, PM-PoS, PA-PoS"]
    csvLabelSeparatedSf = ["nodeCount, SF7-PS-PoS, SF7-PM-PoS, SF7-PA-PoS, SF8-PS-PoS, SF8-PM-PoS, SF8-PA-PoS, SF9-PS-PoS, SF9-PM-PoS, SF9-PA-PoS, SF10-PS-PoS, SF10-PM-PoS, SF10-PA-PoS, SF11-PS-PoS, SF11-PM-PoS, SF11-PA-PoS, SF12-PS-PoS, SF12-PM-PoS, SF12-PA-PoS "]

    pandm = "/ProposedAndModel"
    lrwnpa = "/LorawanPureAloha"

    for edn in edns:
        ps_pos = 0.0
        pm_pos = 0.0
        pa_pos = 0.0
        for occ in sim_occurrence_history:
            sim_res_dir = sim_occurrence_history[occ][edn][pt]

            with open(sim_res_dir + lrwnpa) as lrwnpa_f:
                lrwnpa_content = lrwnpa_f.readlines()
            lrwnpa_content = [x.strip() for x in lrwnpa_content]

            with open(sim_res_dir + pandm) as pandm_f:
                pandm_content = pandm_f.readlines()
            pandm_content = [x.strip() for x in pandm_content]

            pandm_json_r = json2obj(pandm_content[0])
            lrwnpa_json_r = json2obj(lrwnpa_content[0])

            ps_pos += float(pandm_json_r.Proposed.ProbabilityOfSucc)
            pm_pos += float(pandm_json_r.Model.ProbabilityOfSucc)
            pa_pos += float(lrwnpa_json_r.SuccXmt)/edn
        ps_pos /= float(occurrence_count)
        pm_pos /= float(occurrence_count)
        pa_pos /= float(occurrence_count)
        csvAllSf.append(str(edn) + ", " + str(ps_pos) + ", " + str(pm_pos) + ", " + str(pa_pos))

    with open('minPayloadAllDevicePoS.csv', 'a') as minPayloadAllDevicePoS:
        for line in csvAllSf:
            minPayloadAllDevicePoS.write(line + '\n')

    for edn in edns:
        sf_ps_pos = {}
        sf_pm_pos = {}
        sf_pa_pos = {}

        for occ in sim_occurrence_history:
            sim_res_dir = sim_occurrence_history[occ][edn][pt]

            with open(sim_res_dir + lrwnpa) as lrwnpa_f:
                lrwnpa_content = lrwnpa_f.readlines()
            lrwnpa_content = [x.strip() for x in lrwnpa_content]

            with open(sim_res_dir + pandm) as pandm_f:
                pandm_content = pandm_f.readlines()
            pandm_content = [x.strip() for x in pandm_content]

            pandm_json_r = json2obj(pandm_content[0])
            lrwnpa_json_r = json2obj(lrwnpa_content[0])

            proposed_sf_pos = ast.literal_eval(pandm_json_r.Proposed.SfProbabilityOfSucc)
            model_sf_pos = ast.literal_eval(pandm_json_r.Model.SfProbabilityOfSucc)
            lrwnpa_sf_pos = ast.literal_eval(lrwnpa_json_r.SfSuccXmt)
            sf_device_amount = ast.literal_eval(pandm_json_r.SfDeviceAmount)

            sf_ps_pos = dict(Counter(sf_ps_pos)+Counter(proposed_sf_pos))
            sf_pm_pos = dict(Counter(sf_pm_pos) + Counter(model_sf_pos))
            sf_pa_pos = dict(Counter(sf_pa_pos) + Counter({sf: float(lrwnpa_sf_pos[sf])/sf_device_amount[sf] for sf in lrwnpa_sf_pos}))

        sf_ps_pos = {sf: sf_ps_pos[sf]/float(occurrence_count) for sf in sf_ps_pos}
        sf_pm_pos = {sf: sf_pm_pos[sf]/float(occurrence_count) for sf in sf_pm_pos}
        sf_pa_pos = {sf: sf_pa_pos[sf]/float(occurrence_count) for sf in sf_pa_pos}

        line = ""
        for sf in sf_ps_pos:
            line += ", " + str(sf_ps_pos[sf]) + ", " + str(sf_pm_pos[sf]) + ", " + str(sf_pa_pos[sf])
        csvLabelSeparatedSf.append(str(edn) + line)

    with open('minPayloadAllSFDevicePoS.csv', 'a') as minPayloadAllSFDevicePoS:
        for line in csvLabelSeparatedSf:
            minPayloadAllSFDevicePoS.write(line + '\n')


def ackDeviceNumberCase(sim_occurrence_history, edns):
    pt = 'Min'
    occurrence_count = len(sim_occurrence_history)
    csvAck = ["nodeCount, NaiveAggregation, BooleanExpressionAggregation"]
    psoltr = "/ProposedSolutionTraffic"

    for edn in edns:
        ackSizeWOExp = 0
        ackSizeWExp = 0
        for occ in sim_occurrence_history:
            sim_res_dir = sim_occurrence_history[occ][edn][pt]

            with open(sim_res_dir + psoltr) as psoltr_f:
                psoltr_content = psoltr_f.readlines()
            psoltr_content = [x.strip() for x in psoltr_content]

            psoltr_json_r = json2obj(psoltr_content[0])

            ackSizeWOExp += ast.literal_eval(psoltr_json_r.DLAckSzWOExp)
            ackSizeWExp += ast.literal_eval(psoltr_json_r.DLAckSzWExp)

        avgAckSizeWOExp = ackSizeWOExp / float(occurrence_count)
        avgAckSizeWExp = ackSizeWExp / float(occurrence_count)

        csvAck.append(str(edn) + "," + str(avgAckSizeWOExp) + "," + str(avgAckSizeWExp))

    with open('ackDeviceNumberCase.csv', 'a') as ackDeviceNumberCase:
        for line in csvAck:
            ackDeviceNumberCase.write(line + '\n')

def ackPayloadTypeCase(sim_occurrence_history, pts):
    _pt = {'Min': 1, 'Max': 3, 'Avg': 2}
    edn = 5000
    occurrence_count = len(sim_occurrence_history)
    csvAck = ["payloadType, NaiveAggregation, BooleanExpressionAggregation"]
    psoltr = "/ProposedSolutionTraffic"

    for pt in pts:
        ackSizeWOExp = 0
        ackSizeWExp = 0
        for occ in sim_occurrence_history:
            sim_res_dir = sim_occurrence_history[occ][edn][pt]

            with open(sim_res_dir + psoltr) as psoltr_f:
                psoltr_content = psoltr_f.readlines()
            psoltr_content = [x.strip() for x in psoltr_content]

            psoltr_json_r = json2obj(psoltr_content[0])

            ackSizeWOExp += ast.literal_eval(psoltr_json_r.DLAckSzWOExp)
            ackSizeWExp += ast.literal_eval(psoltr_json_r.DLAckSzWExp)

        avgAckSizeWOExp = ackSizeWOExp / float(occurrence_count)
        avgAckSizeWExp = ackSizeWExp / float(occurrence_count)

        csvAck.append(str(_pt[pt]) + "," + str(avgAckSizeWOExp) + "," + str(avgAckSizeWExp))

    with open('ackPayloadTypeCase.csv', 'a') as ackPayloadTypeCase:
        for line in csvAck:
            ackPayloadTypeCase.write(line + '\n')


def performanceMetricsDeviceNumberCase(sim_occurrence_history, edns):
    pt = 'Min'
    occurrence_count = len(sim_occurrence_history)
    csvAck = ["nodeCount, Simulation, ULMsgNm, DLACKNm"]
    lpa = "/LorawanPureAloha"
    psoltr = "/ProposedSolutionTraffic"

    for edn in edns:
        PA_ULMsgNm = 0
        PA_DLACKNm = 0
        PS_ULMsgNm = 0
        PS_DLACKNm = 0
        for occ in sim_occurrence_history:
            sim_res_dir = sim_occurrence_history[occ][str(edn)][pt]

            with open(sim_res_dir + psoltr) as psoltr_f:
                psoltr_content = psoltr_f.readlines()
            psoltr_content = [x.strip() for x in psoltr_content]

            with open(sim_res_dir + lpa) as lpa_f:
                lpa_content = lpa_f.readlines()
                lpa_content = [x.strip() for x in lpa_content]

            psoltr_json_r = json2obj(psoltr_content[0])
            lpa_json_r = json2obj(lpa_content[0])

            PA_ULMsgNm += ast.literal_eval(lpa_json_r.ULMsgCnt)
            PA_DLACKNm += ast.literal_eval(lpa_json_r.DLAckCnt)
            PS_ULMsgNm += ast.literal_eval(psoltr_json_r.ULXmtCnt)
            PS_DLACKNm += ast.literal_eval(psoltr_json_r.DLAckCount)

        avg_PA_ULMsgNm = PA_ULMsgNm / float(occurrence_count)
        avg_PA_DLACKNm = PA_DLACKNm / float(occurrence_count)
        avg_PS_ULMsgNm = PS_ULMsgNm / float(occurrence_count)
        avg_PS_DLACKNm = PS_DLACKNm / float(occurrence_count)

        csvAck.append(str(edn) + "," + "PS" + "," + str(avg_PS_ULMsgNm) + "," + str(avg_PS_DLACKNm))
        csvAck.append(str(edn) + "," + "PA" + "," + str(avg_PA_ULMsgNm) + "," + str(avg_PA_DLACKNm))

    with open('performanceMetricsDeviceNumberCase.csv', 'a') as performanceMetricsDeviceNumberCase:
        for line in csvAck:
            performanceMetricsDeviceNumberCase.write(line + '\n')


def performanceMetricsPayloadTypeCase(sim_occurrence_history, pts):
    _pt = {'Min': 1, 'Max': 3, 'Avg': 2}
    edn = 5000
    occurrence_count = len(sim_occurrence_history)
    csvAck = ["payloadType, Simulation, ULMsgNm, DLACKNm"]
    lpa = "/LorawanPureAloha"
    psoltr = "/ProposedSolutionTraffic"

    for pt in pts:
        PA_ULMsgNm = 0
        PA_DLACKNm = 0
        PS_ULMsgNm = 0
        PS_DLACKNm = 0
        for occ in sim_occurrence_history:
            sim_res_dir = sim_occurrence_history[occ][str(edn)][pt]

            with open(sim_res_dir + psoltr) as psoltr_f:
                psoltr_content = psoltr_f.readlines()
            psoltr_content = [x.strip() for x in psoltr_content]

            with open(sim_res_dir + lpa) as lpa_f:
                lpa_content = lpa_f.readlines()
                lpa_content = [x.strip() for x in lpa_content]

            psoltr_json_r = json2obj(psoltr_content[0])
            lpa_json_r = json2obj(lpa_content[0])

            PA_ULMsgNm += ast.literal_eval(lpa_json_r.ULMsgCnt)
            PA_DLACKNm += ast.literal_eval(lpa_json_r.DLAckCnt)
            PS_ULMsgNm += ast.literal_eval(psoltr_json_r.ULXmtCnt)
            PS_DLACKNm += ast.literal_eval(psoltr_json_r.DLAckCount)

        avg_PA_ULMsgNm = PA_ULMsgNm / float(occurrence_count)
        avg_PA_DLACKNm = PA_DLACKNm / float(occurrence_count)
        avg_PS_ULMsgNm = PS_ULMsgNm / float(occurrence_count)
        avg_PS_DLACKNm = PS_DLACKNm / float(occurrence_count)

        csvAck.append(str(_pt[pt]) + "," + "PS" + "," + str(avg_PS_ULMsgNm) + "," + str(avg_PS_DLACKNm))
        csvAck.append(str(_pt[pt]) + "," + "PA" + "," + str(avg_PA_ULMsgNm) + "," + str(avg_PA_DLACKNm))

    with open('performanceMetricsPayloadTypeCase.csv', 'a') as performanceMetricsPayloadTypeCase:
        for line in csvAck:
            performanceMetricsPayloadTypeCase.write(line + '\n')

def _json_object_hook(d):
    return namedtuple('X', d.keys())(*d.values())


def json2obj(data):
    return json.loads(data, object_hook=_json_object_hook)