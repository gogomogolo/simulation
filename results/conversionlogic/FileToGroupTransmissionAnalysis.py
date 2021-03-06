from results.model.GroupTransmissionAnalysis import GroupTransmissionAnalysis
import util.ListUtil as ListUtil
import parameters.Constants as Constants

class FileToGroupTransmissionAnalysis(object):
    def __init__(self, spreading_factor, group_id):
        self.spreading_factor = spreading_factor
        self.group_id = group_id

    def convert(self, output):
        splitter = '|'
        match_case = "| <SF> : {spreading_factor} | <GroupId> : {group_id} |"\
            .format(spreading_factor=self.spreading_factor, group_id=self.group_id)

        group_device_amount = 0
        attempts = []
        idles = []
        successes = []
        fails = []

        for line in output:
            if match_case in line:
                values = line.split(splitter)
                attempt = int(values[1].split(':')[1].lstrip().rstrip())
                group_device_amount = int(values[4].split(':')[1].lstrip().rstrip())
                idle_amount = int(values[6].split(':')[1].lstrip().rstrip())
                success_amount = int(values[7].split(':')[1].lstrip().rstrip())
                fail_amount = int(values[8].split(':')[1].lstrip().rstrip())
                attempts.append(attempt)
                idles.append(idle_amount)
                successes.append(success_amount)
                fails.append(fail_amount)

        if len(attempts) == 0:
            max_attemp = int(\
                Constants.SIMULATION_LIFE_TIME_IN_SECONDS/\
                Constants.SF_TO_SUPER_GROUP_PERIOD_IN_SEC.get(self.spreading_factor))
            attempts = [x for x in range(1, max_attemp + 1)]
            idles = ListUtil.zero_list(max_attemp)
            successes = ListUtil.zero_list(max_attemp)
            fails = ListUtil.zero_list(max_attemp)

        return GroupTransmissionAnalysis(self.spreading_factor, self.group_id,
                                         group_device_amount, attempts, idles,
                                         successes, fails)
