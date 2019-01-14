from results.model.SuperGroupAnalysis import SuperGroupAnalysis


class FileToSuperGroupAnalysis(object):
    def __init__(self, spreading_factor):
        self.spreading_factor = spreading_factor

    def convert(self, output):
        splitter = '|'
        match_case = "| <SF> : {spreading_factor} |".format(spreading_factor=self.spreading_factor)

        super_group_device_amount = 0
        group_amount = 0

        for line in output:
            if match_case in line:
                values = line.split(splitter)
                super_group_device_amount = int(values[2].split(':')[1].lstrip().rstrip())
                group_amount = int(values[6].split(':')[1].lstrip().rstrip())

        return SuperGroupAnalysis(self.spreading_factor, super_group_device_amount, group_amount)