class SfGroupId(object):
    def __init__(self, sf, group_id):
        self.sf = sf
        self.group_id = group_id
        self.matchcase = "| <SF> : {spreading_factor} | <GroupId> : {group_id} |".\
            format(spreading_factor=sf, group_id=group_id)

    def match_case(self):
        return self.matchcase
